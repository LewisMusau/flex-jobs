from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        strip=False,
        help_text='',  # Set an empty string to hide the help text
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        strip=False,
        help_text='',  # Set an empty string to hide the help text
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
