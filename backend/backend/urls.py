from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import yasg


urlpatterns = [
    path("admin/", admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("api/", include('api.urls')),
] + yasg.urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
