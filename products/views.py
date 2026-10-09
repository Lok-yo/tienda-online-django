from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import calcular_precio_final


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def precio_final(request, pk):
    """Facade: ofrece el cálculo completo mediante una sola petición autenticada."""
    try:
        resultado = calcular_precio_final(pk)
    except Product.DoesNotExist:
        raise NotFound("Producto no encontrado.")
    return Response(resultado)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
