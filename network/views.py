from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Post, User


def index(request):
    posts = Post.objects.all().order_by("timestamp").reverse()
    return render(request, "network/index.html", {"posts": posts})


def post(request):
    fetched_user = User.objects.get(email=request.user.email)

    if request.method == "POST":
        body = request.POST["post-body"]
        new_post = Post.objects.create(user=fetched_user, body=body)
        new_post.save()

        return HttpResponseRedirect(reverse("network:index"))

    return render(request, "network/index.html")


@login_required
def following(request):
    posts = []
    fetched_user = User.objects.get(email=request.user.email)
    fetched_following = User.objects.all().filter(following=fetched_user)

    for follow in fetched_following:
        fetched_posts = list(Post.objects.filter(user=follow).reverse())
        for flat_post in fetched_posts:
            posts.append(flat_post)

    return render(request, "network/following.html", {"posts": posts})


@login_required
def user(request, user_id):
    try:
        logged_in_user = request.user
        current_user = User.objects.get(pk=user_id)
    except User.DoesNotExist as error:
        messages.add_message(request, messages.ERROR, error, extra_tags="bid")
        return HttpResponseRedirect(reverse("network:index"))

    is_followed = (
        current_user.following.all().filter(pk=logged_in_user.pk).exists()
    )

    fetched_followers = (
        User.objects.all().filter(following=current_user).count()
    )
    fetched_following = (
        User.objects.all().filter(followers=current_user).count()
    )
    fetched_posts = Post.objects.filter(user=current_user).reverse()

    if request.method == "POST":
        if "follow" in request.POST:
            is_followed = toggle_followed(logged_in_user, current_user)
            return HttpResponseRedirect(
                reverse("network:user", kwargs={"user_id": user_id})
            )

    return render(
        request,
        "network/user.html",
        {
            "is_followed": is_followed,
            "user": current_user,
            "posts": fetched_posts,
            "following": fetched_following,
            "followers": fetched_followers,
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        request_user = authenticate(
            request, username=username, password=password
        )

        # Check if authentication successful
        if request_user is not None:
            login(request, request_user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "network/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
        except IntegrityError:
            return render(
                request,
                "network/register.html",
                {"message": "Username already taken."},
            )
        login(request, new_user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


def toggle_followed(logged_in_user, current_user):
    # is the logged in user following the current user?
    is_logged_in_user_is_following_current_user = (
        current_user.following.all().filter(pk=logged_in_user.pk).exists()
    )

    if is_logged_in_user_is_following_current_user:
        logged_in_user.followers.remove(current_user)
    else:
        logged_in_user.followers.add(current_user)

    return is_logged_in_user_is_following_current_user
