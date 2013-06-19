#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from uni_form.helpers import FormHelper, Submit, Reset
from oauth2app.models import AccessRange
from apps.account.models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
        ]

class CreateClientForm(forms.Form):
    
    name = forms.CharField(label="Name", max_length=30)
    
    @property
    def helper(self):
        form = CreateClientForm()
        helper = FormHelper()
        reset = Reset('','Reset')
        helper.add_input(reset)
        submit = Submit('','Create Client')
        helper.add_input(submit)
        helper.form_action = '/account/clients'
        helper.form_method = 'POST'
        return helper


class ClientRemoveForm(forms.Form):

    client_id = forms.IntegerField()


class SignupForm(UserCreationForm):
    
    username = forms.EmailField(label="Email")
    
    @property
    def helper(self):
        form = SignupForm()
        helper = FormHelper()
        reset = Reset('','Reset')
        helper.add_input(reset)
        submit = Submit('','Sign Up')
        helper.add_input(submit)
        helper.form_action = '/account/signup'
        helper.form_method = 'POST'
        return helper


class LoginForm(forms.Form):
    
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    @property
    def helper(self):
        form = LoginForm()
        helper = FormHelper()
        reset = Reset('','Reset')
        helper.add_input(reset)
        submit = Submit('','Log In')
        helper.add_input(submit)
        helper.form_action = '/account/login'
        helper.form_method = 'POST'
        return helper

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct username and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data
    

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('profile',)
        
    @property
    def helper(self):
        form = GroupForm()
        helper = FormHelper()
        reset = Reset('','Reset')
        helper.add_input(reset)
        submit = Submit('','Create Group')
        helper.add_input(submit)
        helper.form_action = '/account/groups'
        helper.form_method = 'POST'
        return helper

ROLE_CHOICES = (
    ('family', 'family'),
    ('peers', 'peers'),
    ('care_team', 'care team'),
)
class RoleToProfileForm(forms.Form):
    role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES)
    uid = forms.CharField(label='User ID')
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
