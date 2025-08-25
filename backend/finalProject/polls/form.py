# forms.py
from django import forms
from .models import Comments
from django.contrib.auth.forms import UserCreationForm
from .models import  User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
class ReaderCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name" , "age" ,"password1", "password2"
                      ,"profile_photo" , "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldName in ['password1', 'password2']:
            self.fields[fieldName].help_text = None

class ReaderSignUpForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "age", "password1", "password2","profile_photo"]

    def clean_email(self):    # check if email is already registered
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self): # check if the Tow passwords is match or not
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    def save(self, commit=True): # save the reader info in the DB
        user = super().save(commit=False)
        user.role = "reader"  # force the role
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]
        widgets = {
            "content": forms.TextInput(attrs={
                "class": "form-control md-3",
                "placeholder": "Write your comment here...",
                "row" :"1"
            })
        }


class LikeForm(forms.Form):

    pass

class BookmarkForm(forms.Form):
    pass



