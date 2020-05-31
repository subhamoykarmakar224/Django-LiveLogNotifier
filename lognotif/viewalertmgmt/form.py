from django import forms
from .models import ReAssignment


class FormReAssignment(forms.ModelForm):
    class Meta:
        model = ReAssignment
        fields = [
            'assignment_name', 'assignee', 'assignto'
        ]

