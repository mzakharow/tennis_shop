from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]    # filename.split('.')[1]- расширение файла
    # return "{0}/{1}".format(instance.slug, filename)
    return f'{instance.slug}/{filename}'    #   попробовать такой формат


class Category(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to=image_folder)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # return reverse('category_detail', args=self.slug)
    #     return reverse('category_detail', kwargs={'category_slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, default='')
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)   # max_digits количество знаков ;  decimal_places после запятой
    quantity = models.PositiveIntegerField(blank=True, default=0)
    # size = models.IntegerField(max_length=2)
    available = models.BooleanField(default=True)
    # objects = ProductManager()   # Переопределения менеджера модели

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('product_detail', kwargs={'product_slug': self.slug})


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Cart item for product {self.product.title}'


class Cart(models.Model):
    item = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.item.all():
            cart.item.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.item.all():
            if cart_item.product == product:
                cart.item.remove(cart_item)
                cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.item.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()


# class Address(models.Model):
#     full = models.CharField(max_length=128)
#
#     def __str__(self):
#         return str(self.full)


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')
)

BUYING_TYPE_CHOICES = (
    ('Самовывоз', 'Самовывоз'),
    ('Доставка', 'Доставка')
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # items = models.ManyToManyField(Cart)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=256)
    buying_type = models.CharField(max_length=16, choices=BUYING_TYPE_CHOICES, default='Самовывоз')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES)
    comments = models.TextField()

    def __str__(self):
        return f'Заказ №{str(self.id)}'
