"""Lógica de negocio: estrategias intercambiables para calcular descuentos."""

from decimal import Decimal, ROUND_HALF_UP
from unicodedata import combining, normalize

from .models import Product


class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * Decimal("0.90")


class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * Decimal("0.80")


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio


def obtener_estrategia(categoria_nombre):
    nombre = normalize("NFKD", categoria_nombre.strip().casefold())
    nombre = "".join(letra for letra in nombre if not combining(letra))
    estrategias = {
        "electronica": DescuentoElectronica(),
        "ropa": DescuentoRopa(),
    }
    return estrategias.get(nombre, SinDescuento())


def calcular_precio_final(pk):
    """Consulta el modelo y coordina la estrategia sin modificar el precio guardado."""
    producto = Product.objects.select_related("category").get(pk=pk)
    estrategia = obtener_estrategia(producto.category.name)
    precio = estrategia.calcular(producto.price).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return {
        "producto": producto.name,
        "categoria": producto.category.name,
        "precio_original": format(producto.price, ".2f"),
        "precio_final": format(precio, ".2f"),
    }
