from django.contrib import admin
from shop.models import Category, Brand, Product, CartItem, Cart, Order


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # автоматическое заполнение поле slug в админке


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']     # зададим поля, которые можно редактировать на странице спиcка
    prepopulated_fields = {'slug': ('name', )}   # автоматическое заполнение поле slug в админке


def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')


make_payed.short_description = "Пометить как оплаченные"


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
