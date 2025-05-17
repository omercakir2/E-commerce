from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("SUCCESS!")
            messages.success(request, 'Registered Succesfully!')
            return redirect('register')  # login sayfası varsa
        else:
            print("FORM HATALI:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
def login_view(request):
    # return render(request,'users/login.html')
    return render(request,'TODO.html')

