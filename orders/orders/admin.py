from django.contrib import admin
from .models import Shop, Category, Good, AdditionalGoodParameter


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