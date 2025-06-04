from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage_redirect, name="index"),
    path("home/", views.homepage, name="home"),
    path("create/", views.createListPage, name="create"),
]