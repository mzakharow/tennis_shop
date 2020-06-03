from django.test import TestCase

from shop.models import Brand, Category, CartItem, Product, Cart


class BrandTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Brand.objects.create(name='TestBrand')

    def test_name_label(self):
        brand = Brand.objects.get(id=1)
        name = brand._meta.get_field('name').verbose_name
        print(brand.name)
        self.assertEquals(name, 'name')

    def test_name_max_length(self):
        brand = Brand.objects.get(id=1)
        max_length = brand._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)


class CategoryTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name='Test Category', slug='test-category')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        name = category._meta.get_field('name').verbose_name
        print(category.name)
        self.assertEquals(name, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        print(category.get_absolute_url())
        self.assertEquals(category.get_absolute_url(), '/category/test-category')


class CartTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        category = Category.objects.create(name='Test Category', slug='test-category')
        brand = Brand.objects.create(name='TestBrand')
        product = Product.objects.create(title='Test Product', slug='test-product', brand=brand, category=category, price=22.03)
        CartItem.objects.create(product=product, qty=2, item_total=44.06)

    def test_add_to_cart(self):
        cart = Cart.objects.create()
        cart.cart_total = 44.06
        cart.item.add(CartItem.objects.get(id=1))
        cart.save()
        cart.add_to_cart('test-product', qty=1)
        print(str(cart.cart_total))
        self.assertEquals(cart.cart_total, 66.09)
