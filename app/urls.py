from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing,name="landing"),
    path('signup', views.signup,name="signup"),
    path('login', views.login,name="login"),
    path('home', views.home,name="home"),
    path('logout', views.log_out,name="logout"),
    path('profile', views.profile1,name="profile"),
    path('settings', views.settings,name="settings"),
    path('search', views.search,name="search"),
    path('flow/<un>', views.flow,name="flow"),
]