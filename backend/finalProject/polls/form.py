from django import forms
from django.contrib.auth.forms import UserCreationForm # For basic user creation
from .models import  User


class ReaderCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name" , "age" ,"password1", "password2","profile_photo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldName in ['password1', 'password2']:
            self.fields[fieldName].help_text = None