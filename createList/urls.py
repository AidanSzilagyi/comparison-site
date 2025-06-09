from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage_redirect, name="index"),
    path("home/", views.homepage, name="homepage"),
    path("create/", views.create_list, name="create_list"),
    path("<slug:slug>/info/", views.list_info, name="list_info"),
    path("<slug:slug>/compare/", views.list_compare, name="list_compare"),
    path("<slug:slug>/edit/", views.list_edit, name="list_edit"),
]