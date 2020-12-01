""" Posts URLS."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import posts as post_views

router = DefaultRouter()
router.register(r'users/(?P<username>[a-zA-Z0-9_]+)/posts', post_views.UserPostViewSet, basename='userpost')
router.register(r'posts', post_views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls))
]
