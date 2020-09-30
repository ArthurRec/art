import datetime

from django.contrib.auth.models import (
    AbstractUser, BaseUserManager)
from django.utils.translation import ugettext_lazy as _
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

    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)


class User(AbstractUser):
    """Модель пользователя"""
    objects = UserManager()

    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_admin(self):
        """Пользователь является админом"""
        return self.is_superuser


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.user.username

    def delete_balance(self):
        self.delete()

    def save_balance(self):
        self.save()

    @classmethod
    def search_profile(cls, search_term):
        got_profiles = cls.objects.filter(first_name__icontains=search_term)
        return got_profiles


class Transaction(models.Model):
    description = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateTimeField(default=datetime.datetime.now())
    sender = models.ForeignKey(
        User, related_name='movements_from', on_delete=models.CASCADE)
    addressee = models.ForeignKey(
        User, related_name='movements_to', on_delete=models.CASCADE)