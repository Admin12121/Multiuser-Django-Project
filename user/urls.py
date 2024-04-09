from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('salers', views.salers, name="salers" ),
    path('change_role', views.change_role, name="change_role" ),
    path('signout', views.signout, name='signout'),
]
