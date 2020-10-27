from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .managers import AbstractUserManager


class User(AbstractUser):
    REQUIRED_FIELDS = []
    objects = AbstractUserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    is_vendor = models.BooleanField(default=False)


class Shop(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=50)


class Good(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    shops = models.ManyToManyField(Shop, related_name='categories', blank=True)
    model = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    price_rrc = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


class AdditionalGoodParameter(models.Model):
    good = models.ForeignKey(Good, related_name='additional_parameters', blank=True, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=50)
    value = models.CharField(max_length=50)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', blank=True, on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField()
    adress = models.CharField(max_length=100)