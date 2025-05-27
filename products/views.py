from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')  # change 'login' if your URL name is different
def add_pro_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if name and price:
            Product.objects.create(
                name=name,
                price=price,
                description=description,
                image=image,
                user=request.user  # ✅ Link the product to the logged-in user
            )
            messages.success(request, 'Product added successfully!')
            return redirect('add_pro')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'products/add_product.html')

@login_required(login_url='login') 
def remove_pro_view(request):#remove a product from DB
    return render(request,'TODO.html')

@login_required(login_url='login') 
def list_pro_view(request):#listing products from DB
    query = request.GET.get('q','')
    if request.user.is_authenticated:
        if query:
            products = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query)|Q(user=request.user))
        else:
            products = Product.objects.filter(Q(user=request.user))
    else:
        if query:
            products = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        else:
            products = Product.objects.all()
    
    return render(request,'products/list_product.html',{'products':products,'query':query})
