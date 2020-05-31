from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from alertmgmt.views import view_alert, add_alert_comment, view_add_assignment, view_raw_log


urlpatterns = [
    path('', view_alert, name='view_alert'),
    path('viewraw/<str:src>', view_raw_log, name='view_raw_log'),
    path('addassign/', view_add_assignment, name='view_add_assignment'),
    path('view/add/<str:log_seq_index>/', add_alert_comment, name='add_alert_comment'),
]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
