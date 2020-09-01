from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("post", views.post, name="post"),
    path("post/<int:post_id>", views.post, name="post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("user/<int:user_id>", views.user, name="user"),
]
