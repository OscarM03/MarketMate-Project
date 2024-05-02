from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField

# Create your models here.
class Category(models.Model):
    c_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="bus", alphabet="abcdef123456")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Business(models.Model):
    b_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="bus", alphabet="abcdef123456")
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='marketmate/files/covers', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    phone_no = models.IntegerField(default=0000000000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True, blank=True)
    county = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return self.name
    
class Product(models.Model):
    p_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="bus", alphabet="abcdef123456")
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='marketmate/files/covers', null=True)
    price = models.IntegerField(default=0)
    stock = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name