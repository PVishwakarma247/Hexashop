from django.contrib import admin
from .models import Product, CustomUser


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'stock')
	list_filter = ('category',)
	search_fields = ('name',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
	list_filter = ('is_staff', 'is_superuser', 'is_active')
	search_fields = ('username', 'email')