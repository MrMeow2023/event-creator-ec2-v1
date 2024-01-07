from django.urls import path
from . import views #import from current folder the views.py

urlpatterns = [
    path("", views.index, name='index'),
    path("events", views.start, name='posts-page'),
    path("events/<slug:slug>", views.blog_post, name="post-detail-page"),
    path("create_post", views.new_post, name="new-post-page")
]