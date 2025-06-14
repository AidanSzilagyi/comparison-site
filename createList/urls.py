from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage_redirect, name="index"),
    path("home/", views.homepage, name="homepage"),
    path("create/", views.create_list, name="create_list"),
    path("<slug:slug>/info/", views.list_info, name="list_info"),
    path("<slug:slug>/rank/", views.list_rank, name="list_rank"),
    path("<slug:slug>/edit/", views.list_edit, name="list_edit"),
    path("all-lists/", views.all_lists, name="all_lists")
]