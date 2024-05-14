from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Business, Product, User


class RegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField()
    profile_pic = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove specific validators from the password fields
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic', 'password1', 'password2']

class updateProfileForm(ModelForm):
    """Profile update form"""
    email = forms.EmailField()
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic']

class businessForm(ModelForm):
    """Business creation and update form"""
    # category = forms.CharField(required=True)

    class Meta:
        model = Business
        fields = '__all__'
        exclude = ['b_id', 'votes', 'owner']

class productForm(ModelForm):
    """Product creation and update form"""

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['p_id', 'owner']
