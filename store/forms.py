from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django import forms

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
        
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])

    #     if commit:
    #         user.save()
        
    #     return user
    

