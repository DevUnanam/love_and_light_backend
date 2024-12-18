from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
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

# Logout Endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logs out the user by blacklisting their JWT tokens.
    """
    try:
        # Blacklist all tokens for the logged-in user
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"An error occurred while logging out: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserDetailView(RetrieveAPIView):
    """
    Retrieve a specific user's details (Admin or self).
    """
    queryset = CustomUser.objects.all()  # Use CustomUser model to retrieve users
    serializer_class = UserSerializer  # Serializer class to format the user data
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()  # Admin can access all users
        return CustomUser.objects.filter(id=user.id)  # Regular user can access only their own data

