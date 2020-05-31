from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import alert_mgnt_dash, ack_alert_view, ack_alert_log_view, ack_alert_delete, alert_reassign_view

app_name = 'viewalertmgmt'

urlpatterns = [
    path('dash', alert_mgnt_dash, name="alert_mgnt_dash"),
    path('alert_reassign/<str:alert_name>', alert_reassign_view, name="alert_reassign_view"),
    path('ack_alert$/<str:alert_name>', ack_alert_view, name="ack_alert_view"),
    path('ack_alert_log/<str:alert_name>', ack_alert_log_view, name="ack_alert_log_view"),
    path('ack_alert_delete/<str:alert_name>', ack_alert_delete, name="ack_alert_delete"),
]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
