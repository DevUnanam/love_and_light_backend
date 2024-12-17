from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]