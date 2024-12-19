from rest_framework import serializers
from .models import CustomUser, Property
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Existing UserSerializer for self-registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# New AdminRegisterSerializer for creating Admin or Manager accounts
class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Validate role for Admin or Manager creation.
        """
        role = data.get('role', '').lower()
        if role not in ['admin', 'manager']:
            raise serializers.ValidationError("Role must be 'Admin' or 'Manager'.")
        return data

    def create(self, validated_data):
        """
        Create Admin or Manager user.
        """
        role = validated_data.pop('role').lower()
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )
        # Admins have staff privileges
        user.is_staff = True if role == 'admin' else False
        user.save()
        return user

# Custom Token Serializer for JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        This method customizes the token to include additional claims.
        """
        token = super().get_token(user)
        # Add custom claims to the JWT
        token['role'] = user.role
        token['email'] = user.email
        return token

    def validate(self, attrs):
        """
        Custom validation to allow login with email.
        """
        email = attrs.get('email')  # 'username' is the default key for login
        password = attrs.get('password')

        # Check if user exists by email
        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            pass
        else:
            raise serializers.ValidationError("Invalid email or password")

        # Proceed with JWT validation if login is successful
        return super().validate(attrs)


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'owner', 'address', 'property_type', 'price', 'description']
    
    def create(self, validated_data):
        # Ensures that only authenticated users can add properties
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)