from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.list_type_choices, name="list_type_choices"),
    path("create/manual", views.manual_create_list, name="manual_create"),
    path("create/images-only", views.images_only_create_list, name="images_only_create"),
    path("explore/", views.explore, name="explore"),
    path("recent/", views.recent, name="recent"),
    path("<slug:slug>/info/", views.list_info, name="list_info"),
    path("<slug:slug>/rank/", views.list_rank, name="list_rank"),
    path("<slug:slug>/get-comparisons/", views.get_comparisons, name="get_comparisons"),
    path("<slug:slug>/complete-comparison/", views.complete_comparison, name="complete_comparison"),
    path("<slug:slug>/edit/", views.list_edit, name="list_edit"),
    path("start-login/", views.start_login, name="start-login"),
    path("start-logout/", views.start_logout, name="start_logout"),
    path("all-lists/", views.all_lists, name="all_lists"),
    path("create-profile/", views.create_profile, name="create_profile"),
    path("profile-check/", views.profile_check, name="profile_check"),
    path("profile/", views.my_profile, name="my_profile"),
    path("profile/edit", views.edit_profile, name="edit_profile"),
    path("user/<slug:slug>/", views.view_profile, name="view_profile"),
    path("test/card/", views.list_card_test, name="list_card_test"),
    path("not-found/", views.not_found, name="not_found"),
]