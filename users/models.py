from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import random    
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UniqueIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9 
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            unique_id = random.randint(100000000, 999999999)
            if not User.objects.filter(id=unique_id).exists():
                return unique_id

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = self.generate_unique_id()
            setattr(model_instance, self.attname, value)
        return value

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            registered_at=timezone.now(),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        is_superuser = extra_fields.pop("is_superuser", False)
        return self._create_user(email, password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields, user_type=User.UserTypes.ADMIN
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_type = self.BASE_USER_TYPE
        return super().save(*args, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    class GenderTypes(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
           
    class UserTypes(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    BASE_USER_TYPE = UserTypes.USER
    username = models.CharField(verbose_name="Username", unique=True, max_length=30, null=True, blank=True)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    id = UniqueIDField(primary_key=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    is_staff = models.BooleanField(verbose_name="Staff", default=False)
    registered_at = models.DateTimeField(verbose_name="Registered at", auto_now_add=timezone.now)
    user_type = models.CharField(
        verbose_name=("User Type"), max_length=100, choices=UserTypes.choices, blank=True,
    )
    is_email_verified = models.BooleanField(default=False)
    full_name = models.CharField(verbose_name="Full Name",  max_length=30, null=True, blank=True)
    roll_no = models.CharField(max_length=50, null=True, blank=True, default="")
    phone_no = models.CharField(verbose_name="Phone number", unique=True, max_length=12, null=True, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    is_phone_no_verified = models.BooleanField(verbose_name="Phone number verified", default=False)
    profile_photo = models.ImageField(verbose_name="Profile Pic", blank=True, null=True)
    gender = models.CharField(verbose_name=("Gender Type"), max_length=20,
                              choices=GenderTypes.choices,  blank=True, null=True)
    address = models.TextField(max_length=300, blank=True, null=True)
    pincode=models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    # Fields settings
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    objects = UserManager()
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"