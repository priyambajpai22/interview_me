from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models









class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class User(AbstractUser):
    """User model."""

    username = None
    first_name=None
    last_name=None
    name=models.CharField(max_length=30,blank=True)
    email = models.EmailField(('email address'), unique=True)
    deleted=models.BooleanField(default=False)
    #city=models.CharField(max_length=30, blank=True)
    #profile_pic=models.ImageField(blank=True)
    #phone=models.CharField(max_length=10,blank)
    #termsAccepted=models.BooleanField()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    admin=BaseUserManager()

    def __str__(self):
        return self.email




class InterViewStart(models.Model):
    old_aspirent=models.BooleanField()
    interview_count=models.IntegerField()
    aspirent_user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
