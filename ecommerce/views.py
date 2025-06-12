from django.shortcuts import render
from products.models import Product
from django.db.models import Q
def home(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if query:
        products = products.filter(Q(name__icontains=query)|Q(description__icontains=query)|Q(user__email__icontains=query))
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    return render(request,'home.html',{'products':products})

def custom_404_view(request, exception):
    print("Custom 404 sayfası tetiklendi!")
    return render(request, '404.html', status=404)
