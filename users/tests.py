from unittest.mock import MagicMock, patch
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
        self.assertTrue(self.target_user.check_password(self.user_password))
        self.assertFalse(self.target_user.check_password(self.admin_password))

        login_client = APIClient()
        carlos_login = login_client.post(
            "/api/v1/auth/token/",
            {"email": "carlos.ramirez@utslrc.edu.mx", "password": self.user_password},
            format="json",
        )
        self.assertEqual(carlos_login.status_code, status.HTTP_200_OK)
        self.assertIn("access", carlos_login.data)

    def test_4_public_register_user_endpoint(self):
        """Verifica que POST /api/v1/auth/register/ crea un usuario con password hasheado sin exponerlo."""
        reg_resp = self.client.post(
            "/api/v1/auth/register/",
            {
                "username": "ana_lopez",
                "email": "ana.lopez@utslrc.edu.mx",
                "first_name": "Ana",
                "last_name": "Lopez",
                "matricula": "23304099",
                "carrera": "IDGS 9-2",
                "password": "AnaPassword2026!",
            },
            format="json",
        )
        self.assertEqual(reg_resp.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", reg_resp.data)
        self.assertEqual(reg_resp.data["email"], "ana.lopez@utslrc.edu.mx")
        ana = User.objects.get(email="ana.lopez@utslrc.edu.mx")
        self.assertTrue(ana.check_password("AnaPassword2026!"))

    @patch("users.views.zeep.Client")
    def test_5_soap_country_info_endpoint(self, mock_zeep_client):
        """Verifica el endpoint GET /api/v1/soap/country/?code=MX usando zeep."""
        mock_service = MagicMock()
        mock_info = MagicMock()
        mock_info.sISOCode = "MX"
        mock_info.sName = "Mexico"
        mock_info.sCapitalCity = "Mexico City"
        mock_info.sPhoneCode = "52"
        mock_info.sContinentCode = "AM"
        mock_info.sCurrencyISOCode = "MXN"
        mock_info.sCountryFlag = "http://www.oorsprong.org/WebSamples.CountryInfo/Flags/Mexico.jpg"
        mock_service.FullCountryInfo.return_value = mock_info

        mock_curr = MagicMock()
        mock_curr.sName = "Pesos"
        mock_service.CountryCurrency.return_value = mock_curr

        mock_zeep_client.return_value.service = mock_service

        resp = self.client.get("/api/v1/soap/country/?code=MX")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["country_name"], "Mexico")
        self.assertEqual(resp.data["capital_city"], "Mexico City")
        self.assertEqual(resp.data["currency_iso"], "MXN")
