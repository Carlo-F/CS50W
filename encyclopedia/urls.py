from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("<str:title>", views.entry, name="entry"),
    path("<str:title>/edit", views.edit_entry, name="edit_entry")
]
