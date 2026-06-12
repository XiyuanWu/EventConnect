"""
Event domain models (dev-doc 5.3–5.4).

Uses AUTH_USER_MODEL so it works before accounts views are finished; wire views later.

Scope: browse/post events + comments — no RSVP or participant-tracking models.
"""

from django.conf import settings
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    location = models.CharField(max_length=300)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-starts_at"]

    def __str__(self):
        return self.title


class EventComment(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    # Reply to another comment on the same event (null = top-level comment).
    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.event_id}"
