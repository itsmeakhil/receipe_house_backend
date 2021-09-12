from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from recipe_house_backend.apps.users.managers import UserManager


class Role(models.Model):
    """
    Role Represent Access Level of Each User
    A user may have multiple role
    eg: Admin, Lead, Volunteer,...etc
    """

    ADMIN = 1
    EDITOR = 2
    USER = 3

    ROLE_CHOICES = (
        (ADMIN, _('Admin')),
        (EDITOR, _('Editor')),
        (USER, _('User')),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        """
        calling get_FIELD_display() method
        For every field that has choices set,
        the object will have a get_FOO_display() method,
        where FOO is the name of the field.
        This method returns the “human-readable” value of the field
        """
        return self.get_id_display()


class User(AbstractUser):
    """
    Custom User Model
    """
    username = models.CharField(null=True, blank=True, unique=True,max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128,null=True,blank=True)
    uid = models.CharField(unique=True,max_length=100,null=True,blank=True)
    device_id = models.CharField(unique=True,max_length=100,null=True,blank=True)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    deleted_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name="user_deleted_by",
                                   null=True, blank=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
