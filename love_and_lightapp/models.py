from django.contrib.auth.models import AbstractUser
from django.db import models

# User Roles
ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Tenant', 'Tenant'),
)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Tenant')

    def __str__(self):
        return self.username

