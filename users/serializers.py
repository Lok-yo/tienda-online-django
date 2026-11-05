from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador del modelo User personalizado.
    Corrección de seguridad 1:
    El campo 'password' se configura como write_only=True para que NUNCA se exponga
    el hash de la contraseña en las respuestas GET/POST/PUT/PATCH (incluyendo /api/v1/auth/me/).
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "matricula",
            "carrera",
            "telefono",
            "password",
            "is_active",
            "is_staff",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializador para el registro público de nuevos usuarios (POST /api/v1/auth/register/).
    Incluye validación de longitud mínima de contraseña, hash con make_password y
    write_only=True para jamás devolver la contraseña en la respuesta.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "matricula",
            "carrera",
            "telefono",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
