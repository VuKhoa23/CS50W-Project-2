from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("filter-category", views.filter_category, name="filter-category"),
    path("listing-details/<int:id>", views.listing_details, name="listing-details"),
    path("remove-watchlist/<int:id>", views.remove_watchlist, name="remove-watchlist"),
    path("add-watchlist/<int:id>", views.add_watchlist, name="add-watchlist"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path("add-comment/<int:id>", views.add_comment, name="add-comment"),
]
