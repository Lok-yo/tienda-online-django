import zeep
from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import RegisterUserSerializer, UserSerializer

COUNTRY_INFO_WSDL = (
    "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"
)


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
    Endpoint /api/v1/auth/me/ (Web Service propio protegido con JWT) para obtener
    los datos personales del usuario autenticado sin exponer el campo password.
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


class RegisterUserView(APIView):
    """
    Endpoint público POST /api/v1/auth/register/ para que nuevos usuarios se registren
    desde el frontend en React.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Registrar un nuevo usuario",
        operation_description=(
            "Crea una cuenta de usuario aplicando hash PBKDF2 a la contraseña y "
            "devuelve los datos registrados sin exponer el campo password."
        ),
        request_body=RegisterUserSerializer,
        responses={201: UserSerializer()},
    )
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class SoapCountryInfoView(APIView):
    """
    Endpoint GET /api/v1/soap/country/?code=MX que consume el Web Service SOAP público
    CountryInfoService utilizando la librería zeep.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Consultar información de país vía Web Service SOAP (zeep)",
        operation_description=(
            "Consume el servicio SOAP público CountryInfoService.wso?WSDL mediante zeep "
            "para obtener nombre del país, capital, código telefónico, divisa y bandera."
        ),
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="Código ISO del país (ej. MX, US, ES, CO, JP)",
                type=openapi.TYPE_STRING,
                default="MX",
            )
        ],
    )
    def get(self, request):
        country_code = request.query_params.get("code", "MX").strip().upper() or "MX"
        try:
            client = zeep.Client(wsdl=COUNTRY_INFO_WSDL)
            info = client.service.FullCountryInfo(country_code)
            currency = client.service.CountryCurrency(country_code)
            return Response(
                {
                    "protocol": "SOAP 1.1 / WSDL (consumido desde Django con zeep)",
                    "wsdl_url": COUNTRY_INFO_WSDL,
                    "requested_code": country_code,
                    "iso_code": getattr(info, "sISOCode", country_code),
                    "country_name": getattr(info, "sName", ""),
                    "capital_city": getattr(info, "sCapitalCity", ""),
                    "phone_code": f"+{getattr(info, 'sPhoneCode', '')}",
                    "continent_code": getattr(info, "sContinentCode", ""),
                    "currency_iso": getattr(info, "sCurrencyISOCode", ""),
                    "currency_name": getattr(currency, "sName", ""),
                    "flag_url": getattr(info, "sCountryFlag", ""),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            return Response(
                {
                    "error": "Error al comunicarse con el servidor SOAP externo.",
                    "detail": str(exc),
                    "wsdl_url": COUNTRY_INFO_WSDL,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )
