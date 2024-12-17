from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, AdminRegisterSerializer

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Admin Registration Endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Replaced IsAdminUser with IsAuthenticated
def register_admin(request):
    """
    Endpoint for authenticated users to create Admin or Manager accounts.
    """
    data = request.data
    if not data.get('email') or not data.get('password') or not data.get('role'):
        return Response({"error": "Email, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure role is valid
    role = data.get('role').lower()
    if role not in ['admin', 'manager']:
        return Response({"error": "Role must be 'Admin' or 'Manager'."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    try:
        user = CustomUser.objects.create_user(
            email=data.get('email'),
            password=data.get('password'),
            role=role
        )
        user.is_staff = True if role == 'admin' else False
        user.save()

        serializer = UserSerializer(user)
        return Response({"message": f"{role.capitalize()} account created successfully.", "user": serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)