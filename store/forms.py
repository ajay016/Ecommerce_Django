from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django import forms
from .models import UserProfile
User = get_user_model()

class UserRegistrationForm(forms.ModelForm):

    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password']

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if password:
    #         password_validation.validate_password(password)
    #     return password

    def clean(self):
        cleaned_data = super().clean()
        print('got password')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        # password = self.cleaned_data['password']
        # confirm_password = self.cleaned_data['confirm_password']

        if password and confirm_password and password != confirm_password:
            print('Password do not match ')
            # raise forms.ValidationError('Passwords do not matched')
            msg = 'Passwords do not match'
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            print('Email is already exists')
            raise forms.ValidationError('Email already exists!')

        return email
        
class UserProfileUpdateForm(forms.Form):

    profile_pic = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=255, required=False)
    CHOICES = [('A', 'Male'), ('B', 'Female')]
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)
    street_address = forms.CharField(max_length=255, required=False)
    state = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    zip_code = forms.IntegerField(required=False)
    current_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'gender',
            'street_address',
            'state', 'city',
            'zip_code',
            'current_password',
            'new_password',
            'confirm_new_password'
            ]

