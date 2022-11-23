from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Adminprofile

def ForbiddenUsers(value):
    forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
    if value.lower() in forbidden_users:
        raise ValidationError('invalid name for user, this is a reserved word')

def InvalidUser(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input input-bordered','placeholder':'username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input input-bordered','placeholder':'password'}),required=True)

class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input input-bordered','placeholder':'username'}),max_length=45, required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input input-bordered', 'placeholder':'email'}), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input input-bordered','placeholder':'password'}),label='password', required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input input-bordered','placeholder':'confirm-password'}),label='confirm-password', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsers)
        self.fields['username'].validators.append(InvalidUser)
        self.fields['username'].validators.append(UniqueUser)
        self.fields['email'].validators.append(UniqueEmail)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Password do not match. Try again!'])
        return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):    
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered','placeholder':'old-password'}), label='Old password', required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered','placeholder':'new password'}), label='New password', required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered', 'placeholder':'confirm-password'}), label='confirmed new password', required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] =self.error_class(['Passwords do not match.'])
        return self.cleaned_data

class EditProfileForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput,required=False)
    banner = forms.ImageField(widget=forms.FileInput,required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input text-black w-[450px] bg-white'}), max_length=50, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input text-black w-[450px] bg-white'}), max_length=50, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input text-black w-[450px] bg-white','placeholder':'username'}), required=True)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input text-black w-[450px] bg-white'}), max_length=100, required=False)
    url = forms.URLField(widget=forms.TextInput(), max_length=50, required=False)
    profile_info = forms.CharField(widget=forms.Textarea(attrs={'class':'textarea textarea-bordered text-lg text-black bg-white w-full','placeholder':'Bio'}), max_length=100, required=False)

    class Meta:
        model = Adminprofile
        fields = ('picture', 'banner', 'first_name', 'last_name', 'username', 'location', 'url', 'profile_info')

class ChangePasswordForm(forms.ModelForm):    
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered','placeholder':'old-password'}), label='Old password', required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered','placeholder':'new password'}), label='New password', required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered', 'placeholder':'confirm-password'}), label='confirmed new password', required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] =self.error_class(['Passwords do not match.'])
        return self.cleaned_data



