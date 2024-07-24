from django.contrib.auth.models import AbstractUser
from core.managers import CustomUserManager

class User(AbstractUser):
    email = None
    first_name = None
    last_name = None
    
    objects = CustomUserManager()
