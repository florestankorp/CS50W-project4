from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("user/<int:user_id>", views.user, name="user"),
]
