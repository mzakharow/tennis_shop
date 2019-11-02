from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import shop.urls
from tennis_shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # include(r'^', include('shop.urls')),
    path('', include(shop.urls, namespace='shop')),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
