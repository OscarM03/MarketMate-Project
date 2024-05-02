from django.contrib import admin
from .models import Category, Business, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Business)
admin.site.register(Product)
