from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import OrdersUserChangeForm, OrdersUserCreationForm


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    pass


class OrderedGoodsInLine(admin.TabularInline):
    model = OrderedGoods


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderedGoodsInLine
    ]


@admin.register(User)
class OrderUserAdmin(UserAdmin):
    add_form = OrdersUserCreationForm
    form = OrdersUserChangeForm
    model = User
    list_display = ('email', 'is_vendor',)
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_vendor', 'company')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_vendor', 'company')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)