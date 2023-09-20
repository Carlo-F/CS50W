from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activities/new_activity", views.new_activity, name="new_activity"),
    path("activities/<int:activity_id>", views.activity, name="activity"),
    path("activities/<int:activity_id>/edit_activity", views.edit_activity, name="edit_activity"),
    path("tags", views.tags, name="tags"),
    path("tags/<str:tag>", views.tag, name="tag"),
    path("categories/<str:category>", views.category, name="category"),
    path("latest", views.latest, name="latest"),
    path("popular", views.popular, name="popular"),
    path("favourites", views.favourites, name="favourites"),
    path("my_activities", views.my_activities, name="my_activities"),

    # api
    path("activities", views.activities, name="activities"),
    path("like", views.like, name="like"),
    path("dislike", views.dislike, name="dislike"),
]