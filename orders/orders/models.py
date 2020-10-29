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
    name = models.CharField(max_length=50, verbose_name='Название')
    status = models.BooleanField(default=True, verbose_name='Статус')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Good(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Категория')
    shops = models.ManyToManyField(Shop, related_name='shops', verbose_name='Поставщики')
    model = models.CharField(max_length=50, verbose_name='Модель')
    name = models.CharField(max_length=50, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Оптовая цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Розничная цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class AdditionalGoodParameter(models.Model):
    good = models.ForeignKey(Good, related_name='additional_parameters', blank=True, on_delete=models.CASCADE, verbose_name='Товар')
    parameter = models.CharField(max_length=50, verbose_name='Наименование')
    value = models.CharField(max_length=50, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', blank=True, on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField()
    adress = models.CharField(max_length=100)