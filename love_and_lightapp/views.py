from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from .models import CustomUser, Property
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, AdminRegisterSerializer, PropertySerializer

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Override the post method to return both access and refresh tokens
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh']
        })

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


class UpdateUserView(UpdateAPIView):
    """
    Updates user information (Admin or self).
    """
    queryset = CustomUser.objects.all()  # Queryset to get users
    serializer_class = UserSerializer  # Serializer to format the data
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()  # Admin can access and update any user
        return CustomUser.objects.filter(id=user.id)  # Regular user can access and update only their own data


class DeleteUserView(APIView):
    """
    Deletes a user (Admin or the user itself).
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, pk, format=None):
        try:
            # Retrieve the user by primary key (pk)
            user = CustomUser.objects.get(pk=pk)

            # Check if the requesting user is an Admin or if the user is deleting their own account
            if request.user.is_staff or request.user == user:
                user.delete()
                return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "You do not have permission to delete this user."}, status=status.HTTP_403_FORBIDDEN)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

# Add a new property
class PropertyCreateView(CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Assign property to the authenticated user

# List all properties
class PropertyListView(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

# Retrieve details of a specific property
class PropertyDetailView(RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

# Update property details
class PropertyUpdateView(UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

# Delete a property
class PropertyDeleteView(DestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]