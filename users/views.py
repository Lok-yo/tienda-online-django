from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    """
    CRUD completo de usuarios para administradores.
    Incluye la corrección de los 2 errores de seguridad del manual:
    1. El hash del password jamás se devuelve en la respuesta (write_only=True en UserSerializer).
    2. Al actualizar un usuario sin enviar 'password', se conserva su propia contraseña
       (instance.password) en lugar de sobrescribirla con request.user.password.
    """

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
        password = data.get("password")
        if password:
            data["password"] = make_password(password)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
        password = data.get("password")
        if password:
            data["password"] = make_password(password)
        else:
            # Corrección: eliminamos 'password' del payload para mantener instance.password intacta.
            # NUNCA se asigna request.user.password.
            data.pop("password", None)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class UserView(APIView):
    """
    Endpoint /api/v1/auth/me/ para obtener los datos personales del usuario autenticado
    mediante JWT sin exponer el campo password.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Obtener datos personales del usuario autenticado (JWT)",
        operation_description=(
            "Devuelve la información del usuario propietario del token JWT actual "
            "(incluyendo matrícula y carrera), sin exponer el hash de la contraseña."
        ),
        responses={200: UserSerializer()},
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
