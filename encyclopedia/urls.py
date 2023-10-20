from django.urls import path

from . import views

appname="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entrys, name="entries"),
    path("query/", views.query, name="query"),
    path("newEntry/", views.newEntry, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("<str:title>", views.edit, name="edit"),
    path("random/", views.randomQuery, name="random"),
]
