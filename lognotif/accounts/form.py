from django import forms
from .models import NewUser, ModelNewServer


class FormUser(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['username', 'password', 'role']


class FormNewServer(forms.ModelForm):
    class Meta:
        model = ModelNewServer
        fields = ['servername', 'loglocation', 'createdby']
