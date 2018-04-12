from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(UserCreationForm):
    """
    A class for users
    """
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        # declare the fields we will need in the form
        fields = ('username', 'email', 'password1', 'password2',)
