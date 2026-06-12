from django import forms
from django.contrib import admin

from .models import Event, EventComment


class EventCommentInline(admin.TabularInline):
    model = EventComment
    extra = 0
    readonly_fields = ("created_at",)


class EventAdminForm(forms.ModelForm):
    # Use datetime-local with 5-minute increments for richer time options.
    starts_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "step": 300},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"],
    )

    class Meta:
        model = Event
        fields = "__all__"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ("title", "starts_at", "location", "created_by", "updated_at")
    list_filter = ("starts_at",)
    search_fields = ("title", "location", "description")
    readonly_fields = ("created_at", "updated_at")
    inlines = [EventCommentInline]


@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ("event", "reply_to", "author", "created_at", "is_deleted")
    list_filter = ("is_deleted", "created_at")
    search_fields = ("content",)
