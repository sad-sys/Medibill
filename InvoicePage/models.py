from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class userManager(BaseUserManager):
    def newUser(self, email, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.newUser(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique = True)
    invoices = models.JSONField(null=True)
    sortCode = models.JSONField(null=True)
    phoneNumber = models.IntegerField(null=True)
    address = models.JSONField(null = True)
    company = models.JSONField(null = True)
    bankDetail = models.IntegerField(null=True)

    objects = userManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

