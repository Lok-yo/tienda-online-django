from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Product


class AuthenticatedApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            username="api-test-user",
            password="test-password-123",
        )
        self.client.force_authenticate(user=user)


class CategoryApiTests(AuthenticatedApiTestCase):
    def test_create_category(self):
        response = self.client.post(
            "/api/categories/",
            {"name": "Ropa"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name="Ropa").exists())

    def test_list_categories(self):
        Category.objects.create(name="Electrónica")

        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_names = [category["name"] for category in response.data]
        self.assertEqual(len(response.data), Category.objects.count())
        self.assertIn("Electrónica", returned_names)


class ProductApiTests(AuthenticatedApiTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name="Electrónica")
        self.product = Product.objects.create(
            name="Laptop",
            category=self.category,
            description="Laptop para pruebas",
            price=Decimal("15000.00"),
        )

    def test_create_product(self):
        response = self.client.post(
            "/api/products/",
            {
                "name": "Mouse",
                "category_id": self.category.pk,
                "description": "Mouse inalámbrico",
                "price": "500.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["category"], "Electrónica")
        self.assertTrue(Product.objects.filter(name="Mouse").exists())

    def test_list_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Laptop")
        self.assertEqual(response.data[0]["category"], "Electrónica")

    def test_update_product(self):
        response = self.client.patch(
            f"/api/products/{self.product.pk}/",
            {"name": "Laptop Pro", "price": "18000.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Laptop Pro")
        self.assertEqual(self.product.price, Decimal("18000.00"))

    def test_delete_product(self):
        response = self.client.delete(f"/api/products/{self.product.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_precio_final_autenticado(self):
        # Usamos un JWT real para comprobar también la autenticación del endpoint.
        user = get_user_model().objects.get(username="api-test-user")
        token = str(RefreshToken.for_user(user).access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        ropa = Category.objects.create(name="Ropa")
        camisa = Product.objects.create(
            name="Camisa", category=ropa, description="Camisa de algodón",
            price=Decimal("500.00"),
        )
        generico = Product.crear_con_categoria_default(
            name="Producto genérico", description="Sin descuento",
            price=Decimal("100.00"),
        )
        for producto, esperado in (
            (self.product, "13500.00"), (camisa, "400.00"), (generico, "100.00"),
        ):
            with self.subTest(categoria=producto.category.name):
                response = client.get(f"/api/products/{producto.pk}/precio-final/")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["precio_final"], esperado)
                self.assertEqual(response.data["categoria"], producto.category.name)
                original = producto.price
                producto.refresh_from_db()
                self.assertEqual(producto.price, original)

    def test_precio_final_sin_autenticar(self):
        response = APIClient().get(f"/api/products/{self.product.pk}/precio-final/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Bearer", response["WWW-Authenticate"])
