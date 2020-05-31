from django import forms
from .models import LogFile, LogFilterFields, NewAssignment


class FormLogComment(forms.ModelForm):
    class Meta:
        model = LogFile
        fields= [
            'comments'
        ]


class FormLogFilter(forms.ModelForm):
    class Meta:
        model = LogFilterFields
        fields = [
            'severity_sort', 'timestamp_sort', 'start_date', 'end_date', 'start_time', 'end_time', 'page_no', 'log_src_url'
        ]


class FormAssignment(forms.ModelForm):
    class Meta:
        model = NewAssignment
        fields = [
            'assignment_name', 'assignee', 'assignto', 'ackstatus', 'loglist'
        ]

