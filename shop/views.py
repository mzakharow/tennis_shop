from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.models import Category, Product, Cart, CartItem, Order, Brand
from django.urls import reverse
from shop.forms import OrderForm
from rest_framework import generics, status
from .serializer import ProductSerializer, BrandSerializer


class FilterBrand:
    def get_brand(self):
        return Product.objects.all().values("brand")


def check_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id is not None:
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    else:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
    return cart


def base_view(request):
    new_products = Product.objects.filter(available=True)[0:3]
    best_products = Product.objects.filter(price__gte=3000)[0:3]
    cart = check_cart(request)
    context = {
        'new_products': new_products,
        'best_products': best_products,
        'cart': cart
    }
    return render(request, 'shop/index.html', context)


def contact_view(request):
    products = Product.objects.all().filter(available=True)
    cart = check_cart(request)
    context = {
        'products': products,
        'cart': cart
    }
    return render(request, 'shop/contact.html', context)


def about_view(request):
    products = Product.objects.all().filter(available=True)
    cart = check_cart(request)
    context = {
        'products': products,
        'cart': cart
    }
    return render(request, 'shop/about.html', context)


@login_required
def product_view(request, product_slug):
    cart = check_cart(request)
    product = Product.objects.get(slug=product_slug)
    context = {
        'product': product,
        'cart': cart,
    }
    return render(request, 'shop/product.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    if request.method == "POST":
        products = Product.objects.filter(category=category).filter(brand=request.POST.get("brand"))
    else:
        products = Product.objects.filter(category=category)
    # products = category.product_set.all()  # product_set переменная обратного класса в django
    brands = Brand.objects.all()
    categories = Category.objects.filter(available=True)
    cart = check_cart(request)
    paginator = Paginator(products, 4)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    pages = paginator.get_page(page_num)

    context = {
        'category': category,
        'products': products,
        'brands': brands,
        'categories': categories,
        'cart': cart,
        'pages': pages,
    }
    return render(request, 'shop/category.html', context)


def cart_view(request):
    cart = check_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context)


def add_to_cart_view(request, product_slug):
    cart = check_cart(request)
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.item.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return HttpResponseRedirect(reverse('shop:cart'))


def remove_from_cart_view(request, product_slug):
    cart = check_cart(request)
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.item.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return HttpResponseRedirect(reverse('shop:cart'))


def change_item_qty(request):
    cart = check_cart(request)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    # cart_item.save()
    # new_cart_total = 0.00
    # for item in cart.item.all():
    #     new_cart_total += float(item.item_total)
    # cart.cart_total = new_cart_total
    # cart.save()
    cart.change_qty(qty, item_id)
    return JsonResponse({'cart_total': cart.item.count(),
                         'item_total': cart_item.item_total,
                         'cart_total_price': cart.cart_total})


def order_create_view(request):
    cart = check_cart(request)
    form = OrderForm(request.POST or None)
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'shop/order.html', context)


def make_order_view(request):
    cart = check_cart(request)
    form = OrderForm(request.POST or None)
    context = {
        'cart': cart,
        'form': form,
    }
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        email = form.cleaned_data['email']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            email=email,
            address=address,
            buying_type=buying_type,
            comments=comments
        )
        # new_order = Order()
        # new_order.user = request.user
        # # new_order.items.add(cart)
        # new_order.items = cart
        # new_order.first_name = name
        # new_order.last_name = last_name
        # new_order.phone = phone
        # new_order.address = address
        # new_order.buying_type = buying_type
        # new_order.comments = comments
        # new_order.total = cart.cart_total
        # new_order.email = cart.email
        # new_order.save()
        del request.session['cart_id']
        del request.session['total']

        return HttpResponseRedirect(reverse('shop:confirmation'))
    return render(request, 'shop/order.html', context)


class ListProductView(generics.ListAPIView):
    """
    Providers a get method handler.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class FilterBrandView(FilterBrand, ListView):
    def get_queryset(self):
        queryset = Product.objects.filter(brand__in=self.request.GET.getlist("brand"))
        return queryset
