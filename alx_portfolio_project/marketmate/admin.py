"""Import necessary modules and functions from Django"""
from django.contrib import admin
from .models import Category, Business, Product, User

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Business)
admin.site.register(Product)
