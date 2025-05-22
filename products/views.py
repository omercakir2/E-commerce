from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def add_pro_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Basit doğrulama (istersen daha detaylı yaparız)
        if name and price:
            Product.objects.create(
                name=name,
                price=price,
                description=description,
                image=image
            )
            messages.success(request, 'Product added successfully!')
            return redirect('add_pro')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'products/add_product.html')

def remove_pro_view(request):#remove a product from DB
    return render(request,'TODO.html')
def list_pro_view(request):#listing products from DB
    products = Product.objects.all()
    return render(request,'products/list_product.html',{'products':products})
