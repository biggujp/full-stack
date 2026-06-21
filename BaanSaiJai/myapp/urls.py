from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home,name='home'),
    path('about/', About, name='about'),
    path('products/', AllProducts, name='all_products'),
    path('products/<int:id>/', ProductDetail, name='product_detail'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]

