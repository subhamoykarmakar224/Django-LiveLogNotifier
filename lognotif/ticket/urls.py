from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import view_tickets_list, view_create_tickets, view_delete_tickets, view_change_ticket_status, view_associate_tickets

app_name = 'ticket'

urlpatterns = [
    path('dash', view_tickets_list, name='view_tickets_list'),
    path('create', view_create_tickets, name='view_create_tickets'),
    path('associatetk/<str:assign>', view_associate_tickets, name='view_associate_tickets'),
    path('delete/<str:tid>', view_delete_tickets, name='view_delete_tickets'),
    path('edtstat/<str:tid>', view_change_ticket_status, name='view_change_ticket_status'),
]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
