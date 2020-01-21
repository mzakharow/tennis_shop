from django.urls import path
from rest.views import api_products, api_product_detail, api_brand_detail, api_brands, \
    APIProducts, APIBrands, APIProductDetail

app_name = 'rest'

urlpatterns = [
    # path('api/products/test/', test_api_products),

    # path('products/<int:pk>/', api_product_detail),
    path('products/<int:pk>/', APIProductDetail.as_view()),
    # path('products/', api_products),
    path('products/', APIProducts.as_view()),
    path('brands/<int:pk>/', api_brand_detail),
    # path('brands/', api_brands),
    path('brands/', APIBrands.as_view()),
]