from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    name = forms.CharField(label='ชื่อ-นามสกุล', max_length=100,required=True)
    homenum = forms.CharField(label='บ้านเลขที่', max_length=6,required=True)
    phone = forms.CharField(label='เบอร์โทร', max_length=10,required=True)
    avatar = forms.ImageField(label='รูปประจำตัว', required=False)
    bio = forms.CharField(label='ประวัติส่วนตัว', required=False, widget=forms.Textarea(attrs={'rows': 6}))
    website = forms.URLField(label='เว็บไซต์ส่วนตัว', required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'name',
            'homenum',
            'phone',
            'avatar',
            'bio',
            'website',
        ]
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        