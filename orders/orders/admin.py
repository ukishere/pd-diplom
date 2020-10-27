from django.contrib import admin
from .models import Shop, Category, Good


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    pass