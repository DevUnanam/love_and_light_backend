from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, register_admin, logout_view, UserDetailView, UpdateUserView, DeleteUserView,  PropertyCreateView, PropertyListView, PropertyDetailView, PropertyUpdateView, PropertyDeleteView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register-admin/', register_admin, name='register-admin'),
    path('api/auth/logout/', logout_view, name='logout'),
    path("api/users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("api/users/<int:pk>/update", UpdateUserView.as_view(), name="user-update"),
    path('api/users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete-user'),
    path('api/properties/', PropertyListView.as_view(), name='property-list'),
    path('api/properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('api/properties/<int:pk>/update/', PropertyUpdateView.as_view(), name='property-update'),
    path('api/properties/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property-delete'),
    path('api/properties/create/', PropertyCreateView.as_view(), name='property-create'),
]
