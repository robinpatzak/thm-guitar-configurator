from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_view, name="register"),
    path('account/', views.account_view, name="account")
]