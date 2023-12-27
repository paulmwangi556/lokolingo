from .models import SalerDetail, Product
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from . import models
from django.contrib.admin import widgets                                       

class SalerRegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={}))
	username = forms.CharField(label=("Email / Phone No."),widget=forms.TextInput(attrs={'oninput':'validate()'}))
	# gst = forms.CharField(label=("Business Number"),widget=forms.TextInput(attrs={}))
	shop = forms.CharField(label=("User Name"),widget=forms.TextInput(attrs={}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	password2  = forms.CharField(label=("Re-type Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'shop']

class SalerAddressForm(forms.ModelForm):
	shop_Address = forms.CharField(widget=forms.TextInput(attrs={}))
	locality = forms.CharField(required =True)
	city = forms.CharField(required =True)
	alternate_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Alternate Mobile No(optional)'}), required = False)
	landmark = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Landmark(optional)'}), required = False)
	class Meta:
		model = SalerDetail
		fields = [
			'mobile',
			# 'shop_Name',
			'alternate_mobile',
			'shop_Address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'area',
		]
class UpdateSalerDetailForm(forms.ModelForm):
	class Meta:
		model = SalerDetail
		fields = [
			'photo',
			'mobile',
			# 'shop_Name',
			'gst_Number',
			'alternate_mobile',
			'shop_Address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'area',
		]

class UpdateSalerAccountDetailForm(forms.ModelForm):
	class Meta:
		model = SalerDetail
		fields = [
			'account_Holder_Name',
			'account_Number',
			'ifsc_Code',
			]
  
  
#   skills

class AddSkillForm(forms.ModelForm):
    class Meta:
        model = models.Skill
        fields = [
			"title",
			"category",
			
			"description",
			"thumbnail"
		]
        
class AddTimeSlotForm(forms.ModelForm):
    start_time = forms.TimeField(
        label='Start Time',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    end_time = forms.TimeField(
        label='End Time',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    class Meta:
        model = models.TimeSlots
        fields= [
			"start_time",
			"end_time",
			"date"
		]
        
        
class BookingStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = ['booking_status']