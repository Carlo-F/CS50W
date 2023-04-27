from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("listings/<int:listing_id>",views.listing, name="listing"),
    path("listings/<int:listing_id>/watch", views.watch, name="watch"),
    path("listings/<int:listing_id>/unwatch", views.unwatch, name="unwatch"),
    path("listings/<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("listings/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("listings/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
