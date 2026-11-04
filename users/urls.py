from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

router = DefaultRouter()
router.register(prefix="users", viewset=views.UserApiViewSet, basename="users")

urlpatterns = [
    path("auth/me/", views.UserView.as_view(), name="auth_me"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
