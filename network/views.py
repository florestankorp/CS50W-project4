from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Post, User


def index(request):
    posts = Post.objects.all().order_by("timestamp").reverse()
    page = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/index.html", {"posts": posts})


def post(request):
    fetched_user = User.objects.get(email=request.user.email)

    if request.method == "POST":
        if "post" in request.POST:
            body = request.POST["post-body"]
            new_post = Post.objects.create(user=fetched_user, body=body)
            new_post.save()
            return HttpResponseRedirect(reverse("network:index"))

    return render(request, "network/index.html")


@login_required
def like(request, post_id):
    fetched_user = User.objects.get(email=request.user.email)

    if request.method == "POST":
        if "like" in request.POST:
            toggle_liked(fetched_user, post_id)
            return HttpResponseRedirect(request.headers["Referer"])


@login_required
def following(request):
    posts = []

    page = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)

    fetched_user = User.objects.get(email=request.user.email)
    fetched_following = User.objects.all().filter(following=fetched_user)

    for follow in fetched_following:
        fetched_posts = list(Post.objects.filter(user=follow))
        for flat_post in fetched_posts:
            posts.append(flat_post)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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

    fetched_following = (
        User.objects.all().filter(following=current_user).count()
    )
    fetched_followers = (
        User.objects.all().filter(followers=current_user).count()
    )
    fetched_posts = Post.objects.filter(user=current_user).reverse()
    page = request.GET.get("page", 1)
    paginator = Paginator(fetched_posts, 10)

    if request.method == "POST":
        if "follow" in request.POST:
            is_followed = toggle_followed(logged_in_user, current_user)
            return HttpResponseRedirect(
                reverse("network:user", kwargs={"user_id": user_id})
            )
    try:
        fetched_posts = paginator.page(page)
    except PageNotAnInteger:
        fetched_posts = paginator.page(1)
    except EmptyPage:
        fetched_posts = paginator.page(paginator.num_pages)

    return render(
        request,
        "network/user.html",
        {
            "is_followed": is_followed,
            "logged_in_user": logged_in_user,
            "current_user": current_user,
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
    is_logged_in_user_is_following_current_user = (
        current_user.following.all().filter(pk=logged_in_user.pk).exists()
    )

    if is_logged_in_user_is_following_current_user:
        logged_in_user.followers.remove(current_user)
    else:
        logged_in_user.followers.add(current_user)

    return is_logged_in_user_is_following_current_user


def toggle_liked(logged_in_user, post_id):

    fetched_post = Post.objects.get(pk=post_id)
    has_user_liked_current_post = (
        fetched_post.likes.all().filter(pk=logged_in_user.pk).exists()
    )

    if has_user_liked_current_post:
        fetched_post.likes.remove(logged_in_user)
    else:
        fetched_post.likes.add(logged_in_user)

    return has_user_liked_current_post
