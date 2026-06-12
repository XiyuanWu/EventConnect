import json
import secrets
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify

from .models import Profile


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def placeholder(request):
    return redirect("accounts:login")


def _get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username:
            messages.error(request, "Username is required.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "That username is already taken.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            try:
                validate_password(password)
            except ValidationError as exc:
                for error in exc.messages:
                    messages.error(request, error)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                Profile.objects.create(user=user, display_name=username)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return redirect("accounts:profile")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("accounts:profile")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile_view(request):
    profile = _get_profile(request.user)

    if request.method == "POST":
        request.user.email = request.POST.get("email", "").strip()
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()
        request.user.save()

        profile.display_name = request.POST.get("display_name", "").strip()
        profile.major = request.POST.get("major", "").strip()
        profile.interests = request.POST.get("interests", "").strip()
        profile.bio = request.POST.get("bio", "").strip()
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile")

    return render(request, "accounts/profile.html", {"profile": profile})


def google_login(request):
    google_client_id = getattr(settings, "GOOGLE_CLIENT_ID", "")
    if not google_client_id:
        messages.error(request, "Google login is not configured yet.")
        return redirect("accounts:login")

    state = secrets.token_urlsafe(32)
    request.session["google_oauth_state"] = state
    params = {
        "client_id": google_client_id,
        "redirect_uri": request.build_absolute_uri(reverse("accounts:google_callback")),
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    }
    return redirect(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


def google_callback(request):
    if request.GET.get("state") != request.session.pop("google_oauth_state", None):
        messages.error(request, "Google login state check failed.")
        return redirect("accounts:login")

    code = request.GET.get("code")
    if not code:
        messages.error(request, "Google did not return an authorization code.")
        return redirect("accounts:login")

    try:
        user_info = _fetch_google_user(request, code)
    except Exception:
        messages.error(request, "Could not complete Google login.")
        return redirect("accounts:login")

    email = user_info.get("email", "")
    google_sub = user_info.get("sub")
    if not google_sub:
        messages.error(request, "Google account did not include an ID.")
        return redirect("accounts:login")

    profile = Profile.objects.filter(google_sub=google_sub).select_related("user").first()
    if profile:
        user = profile.user
    else:
        user = _find_or_create_google_user(email, user_info)
        profile = _get_profile(user)
        profile.google_sub = google_sub
        profile.display_name = profile.display_name or user_info.get("name", "")
        profile.save()

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("accounts:profile")


def _fetch_google_user(request, code):
    token_data = {
        "client_id": getattr(settings, "GOOGLE_CLIENT_ID", ""),
        "client_secret": getattr(settings, "GOOGLE_CLIENT_SECRET", ""),
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": request.build_absolute_uri(reverse("accounts:google_callback")),
    }
    token_request = Request(
        GOOGLE_TOKEN_URL,
        data=urlencode(token_data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urlopen(token_request, timeout=10) as response:
        tokens = json.loads(response.read().decode())

    user_request = Request(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    with urlopen(user_request, timeout=10) as response:
        return json.loads(response.read().decode())


def _find_or_create_google_user(email, user_info):
    user = User.objects.filter(email__iexact=email).first()
    if user:
        return user

    base_username = slugify(email.split("@")[0] or user_info.get("name", "google-user")) or "google-user"
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{base_username}-{counter}"

    return User.objects.create_user(
        username=username,
        email=email,
        first_name=user_info.get("given_name", ""),
        last_name=user_info.get("family_name", ""),
        password=None,
    )
