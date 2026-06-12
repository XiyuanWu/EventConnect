from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("create/", views.event_create, name="event_create"),
    path("<str:event_id>/", views.event_detail, name="event_detail"),
    path("<str:event_id>/comments/create/", views.comment_create, name="comment_create"),
]
