from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Business, Product
from .forms import businessForm

# Create your views here.
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exists')

    context = {}
    return render(request, 'marketmate/login-register.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    businesses = Business.objects.filter(Q(county__icontains=q) |
                                         Q(name__icontains=q) |
                                         Q(description__icontains=q) |
                                         Q(category__name__icontains=q)
    )[:12]
    best_seller_businesses = Business.objects.filter(Q(county__icontains=q) |
                                         Q(name__icontains=q) |
                                         Q(description__icontains=q) |
                                         Q(category__name__icontains=q)
    ).order_by('-votes')[:8]
    context = {'businesses': businesses, 'best_seller_businesses': best_seller_businesses}

    return render(request, 'marketmate/index.html', context)

def profilePage(request, id):
    user = User.objects.get(id=id)
    businesses = user.business_set.all()

    if request.user != user:
        return HttpResponse('You are not allowed here!!')

    context = {'user': user, 'businesses': businesses}
    return render(request, 'marketmate/profile.html', context)


def createBusiness(request):
    form = businessForm()

    if request.method == 'POST':
        form = businessForm(request.POST, request.FILES)
        if form.is_valid():
            # category_name = form.cleaned_data['category']

            # category, created = Category.objects.get_or_create(name=category_name)

            business = form.save(commit=False)
            business.owner = request.user
            # business.category = category
            business.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'marketmate/business-form.html', context)

def storesPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    businesses = Business.objects.filter(Q(county__icontains=q) |
                                         Q(name__icontains=q) |
                                         Q(description__icontains=q) |
                                         Q(category__name__icontains=q)
    )

    context = {'businesses': businesses}
    return render(request, 'marketmate/stores.html', context)

def businessPage(request, b_id):
    business = Business.objects.get(b_id=b_id)
    products = business.product_set.all()

    context = {'business': business, 'products': products}

    return render(request, 'marketmate/business.html', context)

def increate_votes(request, b_id):
    business = Business.objects.get(b_id=b_id)
    business.votes += 1
    business.save()

    return redirect('business-page', b_id=b_id)

def categoryPage(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'marketmate/category.html', context)


