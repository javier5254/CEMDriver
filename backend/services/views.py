import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAlistador, IsCliente, IsMotorizado
from coverage.models import Cobertura
from coverage.views import DIAS_ORDEN
from integrations.services import disparar_webhook

from .models import EstadoServicio, Evidencia, MensajeChat, Novedad, Ruta, Servicio, TipoServicio
from .serializers import (
    AsignarRutaSerializer,
    CerrarServicioSerializer,
    MensajeChatSerializer,
    NovedadCreateSerializer,
    NovedadSerializer,
    PlanificarRecoleccionSerializer,
    RutaSerializer,
    ServicioCreateSerializer,
    ServicioSerializer,
)


class RutaViewSet(viewsets.ModelViewSet):
    serializer_class = RutaSerializer

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [IsAuthenticated()]
        return [IsAlistador()]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'MOTORIZADO':
            return Ruta.objects.filter(motorizado=user).order_by('-fecha')
        return Ruta.objects.all().order_by('-fecha')


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ServicioCreateSerializer
        return ServicioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAlistador()]
        if self.action == 'planificar':
            return [IsCliente()]
        if self.action == 'asignar_ruta':
            return [IsAlistador()]
        if self.action in ('recibir_en_centro', 'iniciar_transito', 'cerrar', 'novedad'):
            return [IsMotorizado()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Servicio.objects.all()
        if user.rol == 'CLIENTE':
            return qs.filter(cliente=user)
        if user.rol == 'MOTORIZADO':
            return qs.filter(ruta__motorizado=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user, estado=EstadoServicio.CREADO)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self._notificar('servicio.creado', serializer.instance)
        return Response(ServicioSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    def _motorizado_autorizado(self, servicio: Servicio, user):
        if not servicio.ruta or servicio.ruta.motorizado_id != user.id:
            raise PermissionDenied('Este servicio no esta asignado a tu ruta.')

    def _notificar(self, evento, servicio):
        # disparar_webhook nunca lanza excepciones (ver integrations/services.py);
        # un webhook caido no debe romper la respuesta real de la API.
        disparar_webhook(evento, ServicioSerializer(servicio).data)

    @action(detail=True, methods=['post'], url_path='asignar-ruta')
    def asignar_ruta(self, request, pk=None):
        servicio = self.get_object()
        if servicio.estado != EstadoServicio.CREADO:
            raise ValidationError('Solo se puede asignar ruta a un servicio en estado CREADO.')
        serializer = AsignarRutaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio.ruta = serializer.validated_data['ruta_id']
        servicio.estado = EstadoServicio.ASIGNADO
        servicio.save()
        self._notificar('servicio.asignado', servicio)
        return Response(ServicioSerializer(servicio).data)

    @action(detail=True, methods=['post'], url_path='recibir-en-centro')
    def recibir_en_centro(self, request, pk=None):
        servicio = self.get_object()
        self._motorizado_autorizado(servicio, request.user)
        if servicio.tipo != TipoServicio.ENTREGA:
            raise ValidationError('Solo aplica para servicios de ENTREGA.')
        if servicio.estado != EstadoServicio.ASIGNADO:
            raise ValidationError('El servicio debe estar ASIGNADO para recibirse en centro.')
        servicio.estado = EstadoServicio.RECIBIDO_CENTRO
        servicio.save()
        return Response(ServicioSerializer(servicio).data)

    @action(detail=True, methods=['post'], url_path='iniciar-transito')
    def iniciar_transito(self, request, pk=None):
        servicio = self.get_object()
        self._motorizado_autorizado(servicio, request.user)
        estados_validos_por_tipo = {
            TipoServicio.ENTREGA: (EstadoServicio.RECIBIDO_CENTRO, EstadoServicio.NOVEDAD),
            TipoServicio.RECOLECCION: (EstadoServicio.ASIGNADO, EstadoServicio.NOVEDAD),
        }
        if servicio.estado not in estados_validos_por_tipo[servicio.tipo]:
            raise ValidationError(f'No se puede iniciar transito desde el estado {servicio.estado}.')
        servicio.estado = EstadoServicio.EN_TRANSITO
        servicio.save()
        return Response(ServicioSerializer(servicio).data)

    @action(detail=True, methods=['post'], url_path='cerrar')
    def cerrar(self, request, pk=None):
        servicio = self.get_object()
        self._motorizado_autorizado(servicio, request.user)
        if servicio.estado != EstadoServicio.EN_TRANSITO:
            raise ValidationError('El servicio debe estar EN_TRANSITO para poder cerrarse.')

        serializer = CerrarServicioSerializer(data=request.data, context={'servicio': servicio})
        serializer.is_valid(raise_exception=True)

        if servicio.tipo == TipoServicio.RECOLECCION:
            Evidencia.objects.update_or_create(
                servicio=servicio,
                defaults={
                    'foto': serializer.validated_data['foto'],
                    'firma': serializer.validated_data['firma'],
                },
            )
            servicio.estado = EstadoServicio.RECOLECTADO
        else:
            servicio.estado = EstadoServicio.ENTREGADO
        servicio.save()
        self._notificar(
            'servicio.recolectado' if servicio.tipo == TipoServicio.RECOLECCION else 'servicio.entregado',
            servicio,
        )
        return Response(ServicioSerializer(servicio).data)

    @action(detail=True, methods=['post'], url_path='novedad')
    def novedad(self, request, pk=None):
        servicio = self.get_object()
        self._motorizado_autorizado(servicio, request.user)
        if servicio.estado in (EstadoServicio.ENTREGADO, EstadoServicio.RECOLECTADO, EstadoServicio.DEVUELTO):
            raise ValidationError('El servicio ya esta cerrado, no admite novedades.')

        serializer = NovedadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        novedad = serializer.save(servicio=servicio)

        servicio.estado = EstadoServicio.DEVUELTO if novedad.accion == Novedad.Accion.DEVOLVER else EstadoServicio.NOVEDAD
        servicio.save()
        self._notificar('servicio.novedad', servicio)
        if servicio.estado == EstadoServicio.DEVUELTO:
            self._notificar('servicio.devuelto', servicio)
        return Response(ServicioSerializer(servicio).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='planificar')
    def planificar(self, request):
        serializer = PlanificarRecoleccionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        zona = data['zona']
        fecha_agenda = data['fecha_agenda']
        try:
            cobertura = Cobertura.objects.get(zona=zona)
        except Cobertura.DoesNotExist:
            raise ValidationError('La zona indicada no tiene cobertura configurada.')

        hoy = datetime.date.today()
        if fecha_agenda < hoy + datetime.timedelta(days=cobertura.leadtime_dias):
            raise ValidationError('La fecha de agenda no respeta el leadtime configurado para la zona.')
        if DIAS_ORDEN[fecha_agenda.weekday()] not in cobertura.dias_codigos():
            raise ValidationError('La fecha de agenda cae en un dia no disponible para la zona.')

        servicio = Servicio.objects.create(
            tipo=TipoServicio.RECOLECCION,
            cliente=request.user,
            zona=zona,
            direccion_origen=data['direccion_origen'],
            fecha_agenda=fecha_agenda,
            estado=EstadoServicio.CREADO,
        )
        self._notificar('servicio.creado', servicio)
        return Response(ServicioSerializer(servicio).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], url_path='mensajes')
    def mensajes(self, request, pk=None):
        servicio = self.get_object()
        user = request.user
        es_cliente_dueno = user.rol == 'CLIENTE' and servicio.cliente_id == user.id
        es_motorizado_asignado = user.rol == 'MOTORIZADO' and servicio.ruta and servicio.ruta.motorizado_id == user.id
        if not (es_cliente_dueno or es_motorizado_asignado):
            raise PermissionDenied('El chat es solo entre el cliente del servicio y el motorizado asignado.')

        if request.method == 'GET':
            mensajes = servicio.mensajes.all()
            return Response(MensajeChatSerializer(mensajes, many=True).data)

        serializer = MensajeChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mensaje = serializer.save(servicio=servicio, autor=user)

        data = MensajeChatSerializer(mensaje).data
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f'chat_{servicio.id}', {'type': 'chat_message', 'data': data},
            )

        return Response(data, status=status.HTTP_201_CREATED)
