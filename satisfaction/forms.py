import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from satisfaction.models import *

class RegistrationForm(forms.Form):

	username = forms.CharField(label='Username', max_length=30)
	
	email = forms.EmailField(label='Email')

	password1 = forms.CharField(
		label='Password',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		label='Password (Again)',
		widget=forms.PasswordInput()
	) 

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Passwords do not match.')

	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')

class VideoSaveForm(forms.Form):
	
	url = forms.URLField(
		label='Video URL',
		widget=forms.TextInput(attrs={'size': 64})
	)
	name = forms.CharField(
		label='Name',
		widget=forms.TextInput(attrs={'size': 64})
	)
	
	description = forms.CharField(
		label='Description',
		widget=forms.TextInput(attrs={'size': 64})
	)
	
	category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'))
	
	tags = forms.CharField(
		label='Tags (comma separated)',
		required=False,
		widget=forms.TextInput(attrs={'size': 64})
	)
	#tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('name'))

class SearchForm(forms.Form): 
	query = forms.CharField(
		label='Enter a keyword to search for',
		widget=forms.TextInput(attrs={'size': 32})
	)
