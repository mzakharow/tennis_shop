from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse

from shop.models import Cart, Category
from .forms import LoginForm


def check_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id is not None:
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    else:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart


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
