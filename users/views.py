from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm , EmailLoginForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login,logout
from django.db.models import Q


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("SUCCESS!")
            messages.success(request, 'Registered Succesfully!')
            return redirect('login') 
        else:
            print("FORM HATALI:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)
            messages.success(request, 'Loged in Succesfully!')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print("Email:", email, "Password:", password)
            return redirect('/')
    else:
        form = EmailLoginForm()
    return render(request,'users/login.html',{'form':form})
def logout_view(request):
    logout(request)
    messages.success(request,'Loged out succesfully')
    return redirect('/')

def display_users_view(request):
    query = request.GET.get('q', '')
    if query:
        users = CustomUser.objects.filter(Q(email__icontains=query))
    else:
        users = CustomUser.objects.all()

    return render(request, 'users/display_users.html', {'users': users, 'query': query})
    

def user_detail_by_email(request,user_mail):
    user = get_object_or_404(CustomUser,email=user_mail)
    return render(request,'users/profile.html',{'user':user})