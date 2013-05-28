#-*- coding: utf-8 -*-
from oauth2app.models import *
from django.contrib import admin

from django import forms

CLIENTS_CHOICE_FIELD = forms.ChoiceField(choices = [(client, client.name) for client in Client.objects.all()])
SCOPES_CHOICE_FIELD = forms.MultipleChoiceField(choices = [(scope, scope.key) for scope in AccessRange.objects.all()])

class AccessTokenAdminForm(forms.ModelForm):
    class Meta:
        model = AccessToken
    client = CLIENTS_CHOICE_FIELD
    scope = SCOPES_CHOICE_FIELD

class CodeAdminForm(forms.ModelForm):
    class Meta:
        model = Code
    client = CLIENTS_CHOICE_FIELD
    scope = SCOPES_CHOICE_FIELD

class AuthorizeForm(forms.Form):
    pass
