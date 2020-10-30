from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import OrdersUserManager


class User(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    objects = OrdersUserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    is_vendor = models.BooleanField(default=False, verbose_name='Представитель поставщика')

    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True)
    second_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True)
    third_name = models.CharField(verbose_name='Отчество', max_length=50, blank=True)
    company = models.CharField(verbose_name='Компания', max_length=50, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=50, blank=True)


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    status = models.BooleanField(default=True, verbose_name='Принимает заказы')

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


class AdditionalGoodParameter(models.Model):
    parameter = models.CharField(max_length=50, verbose_name='Наименование')
    value = models.CharField(max_length=50, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return self.parameter+'='+self.value


class Good(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Категория')
    shops = models.ManyToManyField(Shop, related_name='shops', verbose_name='Поставщики')
    parameters = models.ManyToManyField(AdditionalGoodParameter, related_name='parameters', verbose_name='Параметры')
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


class ForWhom(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=50, verbose_name='Дом')
    structure = models.CharField(max_length=50, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=50, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=50, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', blank=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    for_whom= models.ForeignKey(ForWhom, related_name='for_whom', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Куда доставляем')
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    is_delivered = models.BooleanField(default=False, verbose_name='Доставлен')
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтвержден')


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ № '+ str(self.id)


class OrderedGoods(models.Model):
    good_id = models.PositiveIntegerField(verbose_name='Заказанный товар')
    shop_id = models.PositiveIntegerField(verbose_name='Предоставивший поставщик')
    quantity = models.CharField(max_length=50, verbose_name='Количество')
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_goods', blank=True, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    def __str__(self):
        return str(self.good_id)