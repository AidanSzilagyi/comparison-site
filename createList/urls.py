from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage_redirect, name="index"),
    path("home/", views.homepage, name="homepage"),
    path("start-login/", views.start_login, name="start-login"),
    path("create/", views.create_list, name="create_list"),
    path("<slug:slug>/info/", views.list_info, name="list_info"),
    path("<slug:slug>/rank/", views.list_rank, name="list_rank"),
    path("<slug:slug>/get-comparisons/", views.get_comparisons, name="get_comparisons"),
    path("<slug:slug>/complete-comparison/", views.complete_comparison, name="complete_comparison"),
    path("<slug:slug>/edit/", views.list_edit, name="list_edit"),
    path("all-lists/", views.all_lists, name="all_lists"),
    path("create-profile/", views.create_profile, name="create_profile"),
    path("profile-check/", views.profile_check, name="profile_check"),
    path("user/<slug:slug>/", views.view_profile, name="view_profile")
]