import datetime

from django.core.management.base import BaseCommand

from accounts.models import Usuario
from coverage.models import Cobertura
from services.models import EstadoServicio, Ruta, Servicio, TipoServicio


class Command(BaseCommand):
    help = 'Crea usuarios, cobertura y un servicio de demo para CMEDriver.'

    def handle(self, *args, **options):
        self._crear_usuarios()
        self._crear_cobertura()
        self._crear_servicio_demo()
        self.stdout.write(self.style.SUCCESS('Datos de demo creados/actualizados correctamente.'))

    def _crear_usuarios(self):
        usuarios = [
            dict(username='admin', nombre='Ana Administradora', rol='ADMIN',
                 email='admin@cmedriver.local', password='admin1234'),
            dict(username='alistador1', nombre='Luis Alistador', rol='ALISTADOR',
                 email='alistador1@cmedriver.local', password='alistador1234'),
            dict(username='motorizado1', nombre='Mario Motorizado', rol='MOTORIZADO',
                 email='motorizado1@cmedriver.local', password='motorizado1234'),
            dict(username='cliente1', nombre='Carla Cliente', rol='CLIENTE',
                 email='cliente1@cmedriver.local', password='cliente1234'),
        ]
        for datos in usuarios:
            password = datos.pop('password')
            usuario, creado = Usuario.objects.get_or_create(username=datos['username'], defaults=datos)
            if creado:
                usuario.set_password(password)
                usuario.is_staff = usuario.rol == 'ADMIN'
                usuario.is_superuser = usuario.rol == 'ADMIN'
                usuario.save()
                self.stdout.write(f'Usuario creado: {usuario.username} / {password}')

    def _crear_cobertura(self):
        Cobertura.objects.get_or_create(
            zona='Bogota - Chapinero',
            defaults=dict(leadtime_dias=1, dias_disponibles='LUN,MAR,MIE,JUE,VIE'),
        )
        Cobertura.objects.get_or_create(
            zona='Bogota - Suba',
            defaults=dict(leadtime_dias=2, dias_disponibles='LUN,MIE,VIE'),
        )

    def _crear_servicio_demo(self):
        cliente = Usuario.objects.filter(rol='CLIENTE').first()
        motorizado = Usuario.objects.filter(rol='MOTORIZADO').first()
        if not cliente or not motorizado:
            return

        manana = datetime.date.today() + datetime.timedelta(days=1)
        ruta, _ = Ruta.objects.get_or_create(motorizado=motorizado, fecha=manana, defaults={'estado': 'PLANEADA'})

        if not Servicio.objects.filter(direccion_destino='Calle 63 # 10-20, Bogota').exists():
            Servicio.objects.create(
                tipo=TipoServicio.ENTREGA,
                cliente=cliente,
                zona='Bogota - Chapinero',
                direccion_destino='Calle 63 # 10-20, Bogota',
                fecha_agenda=manana,
                estado=EstadoServicio.CREADO,
            )
        if not Servicio.objects.filter(direccion_destino='Carrera 7 # 45-10, Bogota').exists():
            Servicio.objects.create(
                tipo=TipoServicio.ENTREGA,
                cliente=cliente,
                zona='Bogota - Chapinero',
                direccion_destino='Carrera 7 # 45-10, Bogota',
                fecha_agenda=manana,
                estado=EstadoServicio.ASIGNADO,
                ruta=ruta,
            )
        if not Servicio.objects.filter(direccion_origen='Cll 80 #12-30, Bogota').exists():
            Servicio.objects.create(
                tipo=TipoServicio.RECOLECCION,
                cliente=cliente,
                zona='Bogota - Chapinero',
                direccion_origen='Cll 80 #12-30, Bogota',
                fecha_agenda=manana,
                estado=EstadoServicio.CREADO,
            )
