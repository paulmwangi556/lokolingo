from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserDetail


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={}))
    username = forms.CharField(
        label=("Email/Phone"), widget=forms.TextInput(attrs={'oninput': 'validate()'}))
    password1 = forms.CharField(
        label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
    password2 = forms.CharField(
        label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


class UpdateUserDetailForm(forms.ModelForm):
    # dob = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     label='Your Date Field'
    # )
    class Meta:
        model = UserDetail
        fields = [
            "profile_description",
            'rate_per_hour',
            'photo',
            'mobile',
            'alternate_mobile',
            'address',
            'tutoring_experience',
            'identification_document',
            "country",
            'city',
            'sex',
        ]

class UpdateStudentProfileForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = [
            "profile_description",
            'photo',
            'mobile',
            'alternate_mobile',
            'address',
            'identification_document',
            "country",
            'city',
            'sex',
        ]



class UserAddressForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]


class UserAddressForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={}))
    locality = forms.CharField(max_length=100)
    city = forms.CharField(required=True)
    alternate_mobile = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Alternate Mobile No(optional)'}), required=False)
    landmark = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Landmark(optional)'}), required=False)

    class Meta:
        model = UserDetail
        fields = [
            "profile_description",
            'rate_per_hour',
            'photo',
            'mobile',
            'alternate_mobile',
            'address',
            'tutoring_experience',
            'identification_document',
            "country",
            'city',
            'sex',
        ]