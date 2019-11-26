from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse

from shop.forms import RegistrationForm
from shop.models import Cart, Category
from .forms import LoginForm
from shop.views import check_cart


def user_login(request):
    cart = check_cart(request)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('shop:base'))

    context = {
        'form': LoginForm(request.POST),
        'cart': cart,
        'categories': categories
    }
    return render(request, 'account/login.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    cart = check_cart(request)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('shop:base'))
    context = {
        'form': form,
        'cart': cart,
        'categories': categories
    }
    return render(request, 'account/registration.html', context)
