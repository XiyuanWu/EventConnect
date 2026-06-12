"""
Events views (minimal functional MVP).
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .models import Event, EventComment
from accounts.models import Profile
def home(request):
    # This renders a landing page template instead of a list of data
    return render(request, "events/home.html")

def event_list(request):
    events = (
        Event.objects.select_related("created_by")
        .annotate(
            comment_count=Count(
                "comments",
                filter=Q(comments__is_deleted=False),
                distinct=True,
            ),
        )
        .all()
    )
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related("created_by"),
        pk=event_id,
    )
    creator_profile = Profile.objects.filter(user=event.created_by).first()
    root_comments = (
        EventComment.objects.filter(
            event=event,
            is_deleted=False,
            reply_to__isnull=True,
        )
        .select_related("author")
        .prefetch_related(
            Prefetch(
                "replies",
                queryset=EventComment.objects.filter(is_deleted=False)
                .select_related("author")
                .order_by("created_at"),
            )
        )
        .order_by("created_at")
    )
    return render(
        request,
        "events/event_detail.html",
        {"event": event, "root_comments": root_comments,"profile": creator_profile},
    )


@login_required
def event_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        starts_at = request.POST.get("starts_at", "").strip()
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        if title and starts_at and location and description:
            event = Event.objects.create(
                title=title,
                starts_at=starts_at,
                location=location,
                description=description,
                created_by=request.user,
            )
            return redirect("events:event_detail", event_id=event.id)
        return render(
            request,
            "events/event_create.html",
            {"error": "All fields are required."},
        )
    return render(request, "events/event_create.html")


@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.created_by != request.user:
        return HttpResponseForbidden("You can only edit events you created.")
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        starts_at = request.POST.get("starts_at", "").strip()
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        if title and starts_at and location and description:
            event.title = title
            event.starts_at = starts_at
            event.location = location
            event.description = description
            event.save()
            messages.success(request, "Event updated.")
            return redirect("events:event_detail", event_id=event.id)
        return render(
            request,
            "events/event_edit.html",
            {"event": event, "error": "All fields are required."},
        )
    return render(request, "events/event_edit.html", {"event": event})


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.created_by != request.user:
        return HttpResponseForbidden("You can only delete events you created.")
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted.")
        return redirect("events:event_list")
    return redirect("events:event_detail", event_id=event_id)


@login_required
def comment_create(request, event_id):
    if request.method != "POST":
        return redirect("events:event_detail", event_id=event_id)
    event = get_object_or_404(Event, pk=event_id)
    content = request.POST.get("content", "").strip()
    if content:
        EventComment.objects.create(
            event=event,
            author=request.user,
            content=content,
        )
    return redirect("events:event_detail", event_id=event_id)

