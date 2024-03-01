from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .widgets import CustomImageWidget

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(
        attrs = {
            'type': 'date'
        }
    ))
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user',]
        widgets = {
            'gender': forms.RadioSelect(),
            'profile_pic': CustomImageWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = Profile.GENDER_CHOICES
        
