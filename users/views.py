import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm , EmailLoginForm
from django.contrib import messages
from .models import CustomUser
from products.models import Product
from django.contrib.auth import login,logout
from django.db.models import Q
from .utils import send_verification_email,generate_code
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password ,check_password
from django.utils.encoding import force_bytes
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import EmailMessage 


    
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

            result :int = send_verification_email(
                to_email=email,
                subject="Your 2FA Verification Code",
                message=f"Your verification code is: {code}"
            )

            if result == 1:
                print("SUCCESS!")
                messages.success(request, "We've send you a 2fa mail!")
                return redirect('verify_2fa')
            else:
                user.delete()
                messages.error(request,"There has been an error while sending the verification email! Sorry :(")
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
    user= get_object_or_404(CustomUser,email=user_mail)
    products = Product.objects.filter(Q(user=user))
    return render(request,'users/profile.html',{'user':user , 'products':products})



def custom_password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, "users/custom_password_reset_request.html", {"error": "No user with that email."})

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(
            reverse("custom_password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        )

        subject = "Reset your password"
        message = render_to_string("users/password_reset_email.html", {
            "user": user,
            "reset_url": reset_url,
        })

        email_message = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        email_message.content_subtype = "html"  # Bu satır HTML formatı olduğunu belirtir
        email_message.send()

        return redirect("password_reset_done")

    return render(request, "users/custom_password_reset_request.html")

def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 and password1 == password2:
                if check_password(password1, user.password):
                    return render(request, "users/custom_password_reset_confirm.html", {
                        "error": "New password cannot be the same as the old one.",
                        "validlink": True
                    })
                user.password = make_password(password1)
                user.save()
                return redirect("password_reset_complete")
            else:
                return render(request, "users/custom_password_reset_confirm.html", {"error": "Passwords don't match"})

        return render(request, "users/custom_password_reset_confirm.html", {"validlink": True})

    return render(request, "users/custom_password_reset_confirm.html", {"validlink": False})

def password_reset_done(request):
    messages.info(request, "If an account with that email exists, a password reset link has been sent.")
    return render(request, "users/password_reset_done.html")

def password_reset_complete(request):
    messages.success(request, "Your password has been successfully reset. You can now log in.")
    return render(request, "users/password_reset_complete.html")