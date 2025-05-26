import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm , EmailLoginForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login,logout
from django.db.models import Q
from .utils import send_verification_email,generate_code
from django.http import HttpResponse


    
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = form.cleaned_data['email']
            code = generate_code()  # write a simple 6-digit code generator
            seed = str(uuid.uuid4())
            request.session['2fa_seed'] = seed
            request.session['2fa_code'] = code
            request.session['2fa_email'] = email 

            send_verification_email(
                to_email=email,
                subject="Your 2FA Verification Code",
                message=f"Your verification code is: {code}"
            )

            print("SUCCESS!")
            messages.success(request, "We've send you a 2fa mail!")
            return redirect('verify_2fa')
        else:
            print("FORM HATALI:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_2fa_view(request):
    
    if '2fa_seed' not in request.session:
        return redirect('register')  # or show 403 page
    
    if request.method == "POST":
        code_entered = request.POST['code']
        if code_entered == request.session.get('2fa_code'):
            email = request.session.get('2fa_email')
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.save()
            login(request, user)  # Optional: log the user in after verification
            
            request.session.pop('2fa_code', None)
            request.session.pop('2fa_email', None)
            request.session.pop('2fa_seed', None)
            
            
            messages.success(request,"You are verified")
            return redirect('/')
        else:
            messages.error(request,"Code entered is wrong")
    return render(request, 'users/2fa.html')

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