from django import template
from shop.models import Product

register = template.Library()


@register.inclusion_tag('shop/tag/new_products.html')
def get_new_products(count=3):
    products = Product.objects.order_by("-price")[:count]
    return {"new_products": products}
