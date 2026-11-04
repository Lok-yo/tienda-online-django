from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UsersAndJwtSecurityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_password = "AdminUtslrc2026!"
        self.admin = User.objects.create_superuser(
            username="lokiyo",
            email="luis.leon@utslrc.edu.mx",
            password=self.admin_password,
            first_name="Luis Angel",
            last_name="Leon Almazan",
            matricula="23304031",
            carrera="IDGS 9-2",
        )
        self.user_password = "CarlosSecret99!"
        self.target_user = User.objects.create_user(
            username="cramirez",
            email="carlos.ramirez@utslrc.edu.mx",
            password=self.user_password,
            first_name="Carlos",
            last_name="Ramirez",
            matricula="23304088",
            carrera="IDGS 9-2",
        )

    def test_1_jwt_login_with_email(self):
        """Verifica que /api/v1/auth/token/ autentica por correo electrónico y entrega access + refresh."""
        response = self.client.post(
            "/api/v1/auth/token/",
            {"email": "luis.leon@utslrc.edu.mx", "password": self.admin_password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_2_auth_me_returns_profile_without_password_hash(self):
        """
        Verifica la corrección del Error 1:
        /api/v1/auth/me/ devuelve los datos personales (incluyendo matrícula) y NUNCA expone 'password'.
        """
        token_resp = self.client.post(
            "/api/v1/auth/token/",
            {"email": "luis.leon@utslrc.edu.mx", "password": self.admin_password},
            format="json",
        )
        access_token = token_resp.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        me_resp = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(me_resp.data["email"], "luis.leon@utslrc.edu.mx")
        self.assertEqual(me_resp.data["matricula"], "23304031")
        self.assertEqual(me_resp.data["carrera"], "IDGS 9-2")
        self.assertNotIn("password", me_resp.data)

    def test_3_partial_update_without_password_preserves_target_user_password(self):
        """
        Verifica la corrección del Error 2:
        Editar un usuario sin enviar contraseña NO le asigna la contraseña del administrador
        (request.user.password), sino que conserva su propia contraseña original.
        """
        token_resp = self.client.post(
            "/api/v1/auth/token/",
            {"email": "luis.leon@utslrc.edu.mx", "password": self.admin_password},
            format="json",
        )
        admin_access = token_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_access}")

        patch_resp = self.client.patch(
            f"/api/v1/users/{self.target_user.id}/",
            {
                "first_name": "Carlos Alberto",
                "matricula": "23304088",
                "carrera": "IDGS 9-2 (Actualizado)",
            },
            format="json",
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", patch_resp.data)
        self.assertEqual(patch_resp.data["first_name"], "Carlos Alberto")

        self.target_user.refresh_from_db()
        # Su contraseña original sigue funcionando:
        self.assertTrue(self.target_user.check_password(self.user_password))
        # Y NO fue reemplazada por la contraseña del administrador:
        self.assertFalse(self.target_user.check_password(self.admin_password))

        # Además, Carlos puede iniciar sesión por JWT con su propia contraseña:
        login_client = APIClient()
        carlos_login = login_client.post(
            "/api/v1/auth/token/",
            {"email": "carlos.ramirez@utslrc.edu.mx", "password": self.user_password},
            format="json",
        )
        self.assertEqual(carlos_login.status_code, status.HTTP_200_OK)
        self.assertIn("access", carlos_login.data)
