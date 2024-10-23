from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models import Model, EmailField, CharField, Model, RESTRICT, ManyToManyField, BooleanField, OneToOneField
from django_ckeditor_5.fields import CKEditor5Field

from shops.models import Address, Book
from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    is_active = BooleanField(default=False)
    shipping_address = OneToOneField('shops.Address', RESTRICT, null=True, blank=True, related_name='shipping_user')  # Direct reference to Address
    billing_address = OneToOneField('shops.Address', RESTRICT, null=True, blank=True, related_name='billing_user')  # Direct reference to Address

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    wishlist = ManyToManyField('shops.Book', blank=True, related_name='wishlist')



