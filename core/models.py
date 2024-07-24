from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = None
    first_name = None
    last_name = None
