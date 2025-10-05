from django.shortcuts import render,get_object_or_404, redirect
from .models import Card,Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q



@login_required(login_url='login')
def add_to_card(request,pk):
    user = request.user
    #TODO product info product = ...
    product = get_object_or_404(Product, pk=pk)

    if user and product:
        if product.stock  > 0:
            card = Card.objects.create(
                product=product,
                user=user
            )
            messages.success(request,"Added succesfully to your card!")
            product.stock -= 1
            product.save()
        else:
            messages.warning(request,"There is no stock for this product!")
    else:
        messages.error(request,"Something went wrong!!")

    return redirect('home')


def see_card(request):
    if not request.user.is_authenticated:
        messages.error(request,"You need to be loged in to see your card!")
        return redirect('login')

    user_card_items = Card.objects.filter(Q(user=request.user.id))

    total = 0
    for  item in user_card_items:
        total += item.product.price
    
    return render(request,'card/see_card.html',{'items':user_card_items,'total':total})

@login_required(login_url='login')  
def remove_from_card(request,productid,userid):
    product =get_object_or_404(Product , pk = productid)
    
    if product and request.user.id==userid:
        card_item = Card.objects.filter(Q(product=productid)&Q(user=userid))
        if card_item:
            print(f"You tried to delete the card object : {card_item}")
            product = get_object_or_404(Product,pk=card_item[0].product.id)
            if product:
                product.stock += 1
                product.save()
            card_item[0].delete()
        messages.success(request,"Removed succesfully!")
    else:
        messages.warning(request,"Cannot remove!!!")

    return redirect('see_card')

@login_required(login_url='login')
def clear_card(request):
    card_items = Card.objects.filter(Q(user=request.user.id))
    if card_items:
        card_items.delete()
        messages.success(request,"Your order has been succesfully reached to the seller")
    return redirect('see_card')
