from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def Home(request):
    return render(request, 'home.html')

def About(request):
    return render(request, 'about.html')

def AllProducts(request):
    products = Products.objects.all()
    context = {
        'products': products
    }
    return render(request, 'allproducts.html', context)

def ProductDetail(request, id):
    product = get_object_or_404(Products, id=id)
    context = {
        'product': product
    }
    return render(request, 'products.html', context)


from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'ยินดีต้อนรับ {username}! บัญชีผู้ใช้ของคุณถูกสร้างเรียบร้อยแล้ว คุณสามารถเข้าสู่ระบบได้ทันที')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
   if request.method == "POST":
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
           user = form.get_user()
           auth_login(request, user)
           return redirect('all_products')
       else:
           messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
   else:
       form = AuthenticationForm()
   return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to the login page after logout

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    member, created = Member.objects.get_or_create(
        user=request.user
    )
    return render(request, 'profile.html', {
        'member': member
    })

