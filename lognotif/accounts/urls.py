from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import user_profile_view, user_login_view, user_logout_view, user_delete_view, new_server_view, del_server_view

app_name = 'accounts'

urlpatterns = [
    path('login/', user_login_view, name="user_login_view"),
    path('profile/', user_profile_view, name="user_profile_view"),
    path('newserver/', new_server_view, name="new_server_view"),
    path('delete/<str:name>/', user_delete_view, name="user_delete_view"),
    path('logout/', user_logout_view, name="user_logout_view"),
    path('delserver/<str:name>', del_server_view, name="del_server_view"),
]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
