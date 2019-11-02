from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from shop.views import (base_view,
                        product_view,
                        category_view,
                        cart_view,
                        add_to_cart_view,
                        remove_from_cart_view,
                        change_item_qty,
                        make_order_view,
                        order_create_view,
                        contact_view,
                        about_view,
                        account_view,
                        registration_view,
                        login_view,
                        ListProductView)

app_name = 'shop'

urlpatterns = [
    path('category/<slug:category_slug>', category_view, name='category_detail'),
    path('product/<slug:product_slug>', product_view, name='product_detail'),
    path('add_to_cart/<slug:product_slug>', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/<slug:product_slug>', remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty', change_item_qty, name='change_item_qty'),
    path('confirmation/', TemplateView.as_view(template_name='shop/confirmation.html'), name='confirmation'),
    path('order/', order_create_view, name='create_order'),
    path('make_order/', make_order_view, name='make_order'),
    path('cart/', cart_view, name='cart'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('account/', account_view, name='account'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('products/', ListProductView.as_view(), name="product-all"),
    path(r'', base_view, name='base'),
]