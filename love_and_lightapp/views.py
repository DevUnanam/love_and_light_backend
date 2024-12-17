from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import UserSerializer
from .serializers import CustomTokenObtainPairSerializer

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Create your views here.
