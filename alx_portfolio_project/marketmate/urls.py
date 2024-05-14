"""Import necessary modules and functions from Django"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('stores/', views.storesPage, name='stores'),
    path('business/<str:b_id>/', views.businessPage, name='business-page'),
    path('upvotes/<str:b_id>/', views.increate_votes, name='upvotes'),
    path('categories/', views.categoryPage, name='category-page'),
    path('profile/<str:id>/', views.profilePage, name='profile'),
    path('update-profile/<str:id>/', views.profileUpdate, name='profile-update'),
    path('create-business/', views.createBusiness, name='create-business'),
    path('update-business/<str:b_id>/', views.businessUpdate, name='update-business'),
    path('delete-business/<str:b_id>/', views.businessDelete, name='delete-business'),
    path('create-product/', views.createProduct, name='create-product'),
    path('update-product/<str:p_id>/', views.productUpdate, name='update-product'),
    path('delete-product/<str:p_id>/', views.productDelete, name='delete-product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)