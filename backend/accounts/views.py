from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Usuario
from .permissions import IsAdmin
from .serializers import (
    CMEDriverTokenObtainPairSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UsuarioResumenSerializer,
    UsuarioSerializer,
    construir_uid_y_token,
)


class LoginView(TokenObtainPairView):
    serializer_class = CMEDriverTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioResumenSerializer(request.user).data)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('username')
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]


class PasswordResetRequestView(APIView):
    """Solicita el reset: siempre responde 200 (no revela si el correo existe)."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        usuario = Usuario.objects.filter(email__iexact=email).first()
        if usuario:
            uid, token = construir_uid_y_token(usuario)
            enlace = f'{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}'
            send_mail(
                subject='Restablece tu contrasena - CMEDriver',
                message=(
                    f'Hola {usuario.nombre or usuario.username},\n\n'
                    f'Solicitaste restablecer tu contrasena en CMEDriver.\n'
                    f'Entra a este enlace para elegir una nueva (valido por tiempo limitado):\n\n'
                    f'{enlace}\n\n'
                    f'Si no fuiste tu, ignora este correo.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[usuario.email],
            )

        return Response({'detail': 'Si el correo esta registrado, se envio un enlace de restablecimiento.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['usuario']
        usuario.set_password(serializer.validated_data['new_password'])
        usuario.save()
        return Response({'detail': 'Contrasena actualizada correctamente.'}, status=status.HTTP_200_OK)
