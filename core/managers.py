from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)