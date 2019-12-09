from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import registration_view, account_view
from . import views

app_name = 'account'

urlpatterns = [
    path('', account_view, name='account'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),
    path('registration/', registration_view, name='registration'),
]