from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from .models import Place, Profile

from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_admin')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='User Name')
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'username'})
        self.fields['password'].widget.attrs.update({'id': 'password'})
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
        
class PlaceForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Place
        fields = ('name', 'detail', 'latitude', 'longitude', 'image')
        
class ProfileSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('bio', 'profileimg', 'location')
        

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        
