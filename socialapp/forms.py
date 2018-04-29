from django import forms
from django.contrib.auth.models import User
from socialapp.models import User_Personal
from django.core import validators
from django.core.exceptions import ValidationError


def validate_gender(value):
    if str(value).upper() != "MALE" and str(value).upper() != "FEMALE":
        print("gender should be Male or Female")
        raise forms.ValidationError("gender should be Male or Female")



class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on','placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on','placeholder':'Last Name'}))

    username = forms.CharField(label='User Name',
                           widget=forms.TextInput(attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on','placeholder':'Username'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on','placeholder':'Email'}))
    password=forms.CharField(label='Password',
                            widget=forms.PasswordInput(attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on','placeholder':'Password'}))

    class Meta:
        model=User
        fields=('first_name','last_name','username','email','password')


    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")






class PersonalInfoForm(forms.ModelForm):
    dob = forms.CharField(label='Date of Birth',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on',
                                            'placeholder': 'Date of Birth'}))
    gender = forms.CharField(label='Gender',validators=[validate_gender],
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on',
                                           'placeholder': 'Gender'}))

    city = forms.CharField(label='City',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on',
                                          'placeholder': 'City'}))
    country = forms.CharField(label='Country',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control input-group-lg', 'autocomplete': 'on',
                                      'placeholder': 'Country'}))


    class Meta:
        model=User_Personal
        fields=('dob','gender','city','country')










