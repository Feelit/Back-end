from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path('', include(('feelit.users.urls', 'users'), namespace='users')),
    path('', include(('feelit.posts.urls', 'posts'), namespace='posts')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
