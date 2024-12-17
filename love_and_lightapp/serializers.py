from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Custom validation to allow login with email
        email = attrs.get('username')  # 'username' is the default key for login
        password = attrs.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            attrs['username'] = user.username  # Replace with actual username
        else:
            raise serializers.ValidationError("Invalid email or password")

        return super().validate(attrs)
