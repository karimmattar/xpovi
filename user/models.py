from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid

from user.managers import CustomUserManager


class TimeStamp(models.Model):  # Base Model
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimeStamp):    # User Model
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',
                       'first_name',
                       'last_name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        email = str(self.email).lower()
        fname = str(self.first_name).title()
        lname = str(self.last_name).title()
        self.email = email
        self.first_name = fname
        self.last_name = lname
        super(User, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at', 'email')
        indexes = [
            models.Index(fields=['email', 'uuid'])
        ]
