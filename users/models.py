from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, cpf, name, lojista, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        if not cpf:
            raise ValueError(_("The cpf must be set"))
        if not name:
            raise ValueError(_("The name must be set"))      
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, name=name, lojista=lojista, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False, max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    cpf = models.CharField(("CPF"), unique=True, blank=False, null=False, max_length=11)
    name = models.CharField(_("full name"), blank=False, null=False, max_length=150)
    lojista = models.BooleanField(default=False, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


