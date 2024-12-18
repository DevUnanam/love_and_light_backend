from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, register_admin, logout_view, UserDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register-admin/', register_admin, name='register-admin'),
    path('api/auth/logout/', logout_view, name='logout'),
    path("api/users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
