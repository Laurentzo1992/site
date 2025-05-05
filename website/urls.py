
from django.contrib import admin
from django.urls import path, include
from  django.conf.urls.static import  static
from  django.conf import settings


""" urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('mentors.urls')),
    path('tinymce/', include('tinymce.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) """

urlpatterns = []
if settings.ADMIN_ENABLED is True:
    urlpatterns += [path('admin/', admin.site.urls),]


urlpatterns += [
     path('', include('mentors.urls')),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)