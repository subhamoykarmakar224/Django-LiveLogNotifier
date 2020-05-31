from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import open_new_window_view, quit_app_view

app_name = 'filemenu'

urlpatterns = [
    path('new', open_new_window_view, name='open_new_window_view'),
    path('quitapp', quit_app_view, name='quit_app_view')
]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
