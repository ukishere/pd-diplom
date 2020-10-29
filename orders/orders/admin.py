from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Shop, Category, Good, AdditionalGoodParameter
from .forms import OrdersUserChangeForm, OrdersUserCreationForm


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ParametersInLine(admin.TabularInline):
    model = AdditionalGoodParameter


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    inlines = [
        ParametersInLine
    ]

@admin.register(User)
class OrderUserAdmin(UserAdmin):
    add_form = OrdersUserCreationForm
    form = OrdersUserChangeForm
    model = User
    list_display = ('email', 'is_vendor',)
    list_filter = ('email', 'is_vendor',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_vendor',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_vendor',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)