from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Product , ProductImage
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def add_pro_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')  # Çoklu dosya

        if name and price:
            product = Product.objects.create(
                name=name,
                price=price,
                description=description,
                user=request.user
            )

            for i, image in enumerate(images):
                if i >= 5:  # En fazla 5 resim
                    break
                ProductImage.objects.create(product=product, image=image)

            messages.success(request, 'Product added successfully with images!')
            return redirect('add_pro')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'products/add_product.html')

@login_required(login_url='login') 
def remove_pro_view(request):#remove a product from DB
    return render(request,'TODO.html')

def remove_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # 🔐 Sadece ürün sahibi silebilmeli
    if product.user != request.user:
        messages.error(request, "❌ You can't delete this product.")
        return redirect('/')

    # ✅ Sadece POST ile silinebilir
    if request.method == 'POST':
        product.delete()
        messages.success(request, "✅ Product deleted successfully.")
        return redirect('list_pro')  # kendi sayfana göre ayarla

    # ❌ Eğer GET ile geldiyse uyarı ver
    messages.warning(request, "⚠️ You must send a POST request to delete.")
    return redirect('list_pro')

@login_required(login_url='login') 
def list_pro_view(request):#listing products from DB
    query = request.GET.get('q','')
    if request.user.is_authenticated:
        if query:
            products = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        else:
            products = Product.objects.filter(Q(user=request.user))
    else:
        if query: # This part is for unauthenticated users
            products = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        else:
            products = Product.objects.all()
    
    return render(request,'products/list_product.html',{'products':products,'query':query})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase-stock":
            product.stock += 1
            product.save()
        elif action == "decrease-stock":
            if product.stock > 0:
                product.stock -= 1
                product.save()

        # Reload the updated product instance
        product.refresh_from_db()

    print("STOCK:" + str(product.stock))
    return render(request, 'products/product_detail.html', {'product': product})


def add_stock_view(pk):
    product = get_object_or_404(Product, pk=pk)

    if product.stock >= 0:
        product.stock += 1
        product.save()
        print("ARTTIRDIM")


def remove_stock_view(pk):
    product = get_object_or_404(Product, pk=pk)

    if product.stock > 0:
        product.stock -= 1
        product.save()
        print("ARTTIRDIM")

    
