from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,  name="home"),

    path('login', views.log_in, name="login"),
    # path('logout', views.logout, name="logout"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('register', views.register, name="register"),
]