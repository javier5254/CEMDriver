from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre', 'rol', 'telefono', 'email', 'is_active', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario(**validated_data)
        usuario.set_password(password or Usuario.objects.make_random_password())
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UsuarioResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre', 'rol']


class CMEDriverTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = user.rol
        return token

    def validate(self, attrs):
        # Permite iniciar sesion con username o con correo (RF-19): si el
        # identificador recibido es un correo registrado, lo resolvemos al
        # username real antes de que simplejwt valide las credenciales.
        identificador = attrs.get(self.username_field)
        if identificador and '@' in identificador:
            usuario = Usuario.objects.filter(email__iexact=identificador).first()
            if usuario:
                attrs[self.username_field] = usuario.username

        data = super().validate(attrs)
        data['user'] = UsuarioResumenSerializer(self.user).data
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])

    def validate(self, attrs):
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        try:
            user_id = force_str(urlsafe_base64_decode(attrs['uid']))
            usuario = Usuario.objects.get(pk=user_id)
        except (Usuario.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError('Enlace de restablecimiento invalido.')

        if not default_token_generator.check_token(usuario, attrs['token']):
            raise serializers.ValidationError('El enlace ya expiro o no es valido. Solicita uno nuevo.')

        attrs['usuario'] = usuario
        return attrs


def construir_uid_y_token(usuario):
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = default_token_generator.make_token(usuario)
    return uid, token
