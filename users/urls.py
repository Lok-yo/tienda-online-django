from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

router = DefaultRouter()
router.register(prefix="users", viewset=views.UserApiViewSet, basename="users")

urlpatterns = [
    path("auth/me/", views.UserView.as_view(), name="auth_me"),
    path("auth/register/", views.RegisterUserView.as_view(), name="auth_register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("soap/country/", views.SoapCountryInfoView.as_view(), name="soap_country_info"),
    path("", include(router.urls)),
]
