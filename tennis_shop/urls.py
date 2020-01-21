from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import rest.urls
import shop.urls
import account.urls
from tennis_shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(account.urls, namespace='account')),
    path('', include(shop.urls, namespace='shop')),
    path('api/', include(rest.urls, namespace='rest')),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
