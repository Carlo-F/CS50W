from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activity/<int:activity_id>", views.activity, name="activity"),
    path("tags", views.tags, name="tags"),
    path("tags/<str:tag>", views.tag, name="tag"),
    path("categories/<str:category>", views.category, name="category"),
    path("latest", views.latest, name="latest"),
    path("popular", views.popular, name="popular"),

    # api
    path("activities", views.activities, name="activities"),
]