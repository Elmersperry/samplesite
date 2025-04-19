from django.contrib import admin
from django.urls import path, include

from bboard.urls import app_name
from bboard.views import index, about, add_bb, update_bb, read_bb, delete_bb
from samplesite import settings
from django.conf.urls.static import static

app_name='bboard'
urlpatterns = [
    path('', index, name='index'),
    path('bboard/', include('bboard.urls')),
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('users/', include('users.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)