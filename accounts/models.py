from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core import validators
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user model manager
    """
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault('is_admin', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Суперпользователь должен иметь is_admin=True.')

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
    Custom User Model
    """
    username = models.CharField(max_length=255, unique=True, verbose_name='Username')
    email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False, verbose_name='Email')
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='User First Name')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='User Last Name')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

