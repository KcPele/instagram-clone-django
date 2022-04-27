from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser, UserManager)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Use the given user name 、 Email and password create and save users .
        """
        # without username Throw an exception
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given username must be set')
        # Standardized e-mail , If you look at the source code, you'll find that it's using @ Segmentation
        email = self.normalize_email(email)
        # Standardized user names
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        # Set the password for the user , Convert plain text passwords to hash values for database storage
        user.set_password(password)
        # Save the user
        user.save(using=self._db)
        return user
    def create_user(self, username, email=None, password=None, **extra_fields):
    # Set up is_staff The default value is False,is_superuser The default value is False
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)
    def create_superuser(self, username, email, password, **extra_fields):
        # Set up is_staff The default value is True,is_superuser The default value is True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # If you call this method ,is_staff It has to be for True, Otherwise, an exception will be thrown
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        # If you call this method ,is_superuser It has to be for True, Otherwise, an exception will be thrown
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, TrackingModel):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    email_verified = models.BooleanField(_('email_verified'), default=False,
        help_text=_('Designates whether the user email is verified '))
    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    @property
    def token(self):
        return ''