from django import forms
from .models import Ticket


class FormNewTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields= [
            'ticket_id', 'ticket_name', 'assignment_name',
            'author', 'createdon', 'comments'
        ]
