from django.shortcuts import render
from .forms import LoginForm,SignupForm,ChangePasswordForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse('inactive account')
            else:
                return HttpResponse('invalid login')
    else:
        form = LoginForm()
    
    context = {'form': form,}
    return render(request, 'authentication/login.html', context)

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('authy:edit-profile')
    else:
        form = SignupForm()

    context = {
        'form':form,
    }
    return render(request, 'authentication/register.html', context)

@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')

    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form':form,
    }
    return render(request, 'authentication/change_password.html', context)

def PasswordChangeDone(request):
    return render(request, 'authentication/change_password_done.html')
