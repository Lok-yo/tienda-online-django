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
