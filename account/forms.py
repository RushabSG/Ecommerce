from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        # make email field required
        self.fields["email"].required = True

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already present")

        if len(email) >= 350:
            raise ValidationError("Email length too long")

        return email


# login form
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# update form
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ["password1", "password2"]

    def clean_email(self):

        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Email is already present")

        if len(email) >= 350:
            raise ValidationError("Email length too long")

        return email
