from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(max_length=100, widget=forms.TimeInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email here!'}))

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'

        # setting the field labels to empty
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Enter password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Confirm password'})
        # seeting the placeholder text for the password help_text
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''
        # Setting the widget for the password 1 and 2 with form-control
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username',
                  'email', 'password1', 'password2')
        widgets = {'username': forms.TextInput(
            attrs={'placeholder': 'Please enter your username'}), }
