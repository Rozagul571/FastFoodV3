from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        if not password:
            raise ValueError("Password must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone_number, password, **extra_fields)