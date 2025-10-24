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
    username = forms.CharField(max_length=300, widget=forms.TextInput(attrs={
        'class': 'mt-1 focus:ring-gray-300 focus:border-gray-300 block w-full sm:text-sm border border-[#594100] rounded p-2 px-4',
        'placeholder': 'ชื่อผู้ใช้'
        }),
        label='ชื่อผู้ใช้',
        required=True,
        error_messages={
            'unique': 'ชื่อผู้ใช้นี้ถูกใช้งานแล้ว กรุณาเลือกชื่อผู้ใช้อื่น',
            'required': 'กรุณาระบุชื่อผู้ใช้'
        }
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'mt-1 focus:ring-gray-300 focus:border-gray-300 block w-full sm:text-sm border border-[#594100] rounded p-2 px-4',
        'placeholder': 'example@gmail.com'
        }),
        label='อีเมล',
        help_text='กรุณาระบุที่อยู่อีเมลที่ถูกต้อง', 
        required=True, 
        error_messages={
            'required': 'กรุณาระบุที่อยู่อีเมล', 
            'invalid': 'รูปแบบอีเมลไม่ถูกต้อง',
            'unique': 'อีเมลนี้ถูกใช้งานแล้ว'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 focus:ring-gray-300 focus:border-gray-300 block w-full sm:text-sm border border-[#594100] rounded p-2 px-4',
            'placeholder': '••••••••'
        })
        self.fields['password1'].label = 'รหัสผ่าน'

        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 focus:ring-gray-300 focus:border-gray-300 block w-full sm:text-sm border border-[#594100] rounded p-2 px-4',
            'placeholder': '••••••••'
        })
        self.fields['password2'].label = 'ยืนยันรหัสผ่าน'
        self.fields['password2'].error_messages = {
            'password_mismatch': 'รหัสผ่านไม่ตรงกัน'
        }

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
        
