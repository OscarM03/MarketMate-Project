from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Business, Product, User
from .forms import businessForm, productForm, RegistrationForm, updateProfileForm

# Create your views here.
def loginPage(request):
    """Authenticate the user and allow login."""
    page = 'login'
    
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
    return render(request, 'marketmate/login.html', context)
    
def logoutUser(request):
    """Logout the user."""
    logout(request)
    return redirect('home')

def registerPage(request):
    """Render registration form and process registration."""
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.profile_pic = request.FILES.get('profile_pic')
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'form': form}
    return render(request, 'marketmate/register.html', context)

def home(request):
    """Render the home page with business listings and best sellers."""
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

@login_required(login_url='login')
def profilePage(request, id):
    """Render user profile page with associated businesses and product counts."""
    user = User.objects.get(id=id)
    businesses = user.business_set.all()
    business_count = businesses.count()
    products_count = 0
    for business in businesses:
        products = business.product_set.all()
        count = products.count()
        products_count += count

    if request.user != user:
        return HttpResponse('You are not allowed here!!')

    context = {'user': user, 'businesses': businesses, 'business_count': business_count, 'products_count':products_count}
    return render(request, 'marketmate/profile.html', context)

@login_required(login_url='login')
def profileUpdate(request, id):
    """Render and process profile update form."""
    user = User.objects.get(id=id)
    form = updateProfileForm(instance=user)

    if request.method == 'POST':
        form = updateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)
        
    context = {'form': form}
    return render(request, 'marketmate/updateprofile.html', context )



@login_required(login_url='login')
def createBusiness(request):
    """Render and process form to create a new business."""
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
            return redirect('profile', request.user.id)

    context = {'form': form}
    return render(request, 'marketmate/business-form.html', context)

@login_required(login_url='login')
def businessUpdate(request, b_id):
    """Render and process form to update a business."""
    business = Business.objects.get(b_id=b_id)
    form = businessForm(instance=business)

    if request.method == 'POST':
        form = businessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business-page', business.b_id)
        
    context = {'form': form}
    return render(request, 'marketmate/business-form.html', context)

@login_required(login_url='login')
def businessDelete(request, b_id):
    """Delete a business."""
    business = Business.objects.get(b_id=b_id)
    
    if request.method == 'POST':
        business.delete()
        return redirect('profile', business.owner.id)
    
    return render(request, 'marketmate/delete.html', {'obj': business})


@login_required(login_url='login')
def createProduct(request):
    """Render and process form to create a new product."""
    form = productForm()
    product = None

    if request.method == 'POST':
        form = productForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            if request.user == product.business.owner:
                product.save()
            else:
                return HttpResponse("Please select your business")
            return redirect('business-page', product.business.b_id)

    business = None
    if product:
        business = Business.objects.get(b_id=product.business.id)

    context = {'form': form, 'business': business}
    return render(request, 'marketmate/business-form.html', context)

@login_required(login_url='login')
def productUpdate(request, p_id):
    """Render and process form to update a product."""
    product = Product.objects.get(p_id=p_id)
    form = productForm(instance=product)

    if request.method == 'POST':
        form = productForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('business-page', product.business.b_id)
        
    context = {'form': form}
    return render(request, 'marketmate/business-form.html', context)

@login_required(login_url='login')
def productDelete(request, p_id):
    """Delete a product."""
    product = Product.objects.get(p_id=p_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('business-page', product.business.b_id)
    
    return render(request, 'marketmate/delete.html', {'obj': product})


def storesPage(request):
    """Render the stores page with filtered business listings."""
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    businesses = Business.objects.filter(Q(county__icontains=q) |
                                         Q(name__icontains=q) |
                                         Q(description__icontains=q) |
                                         Q(category__name__icontains=q)
    )

    context = {'businesses': businesses}
    return render(request, 'marketmate/stores.html', context)

def businessPage(request, b_id):
    """Render the page for a specific business with its associated products."""
    business = Business.objects.get(b_id=b_id)
    products = business.product_set.all()

    context = {'business': business, 'products': products}

    return render(request, 'marketmate/business.html', context)

def increate_votes(request, b_id):
    """Increase votes for a business."""
    business = Business.objects.get(b_id=b_id)
    business.votes += 1
    business.save()

    return redirect('business-page', b_id=b_id)

def categoryPage(request):
    """Render the category page with all categories."""
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'marketmate/category.html', context)


