from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile, Address


class SignUpForm(UserCreationForm):
    PUBLIC_ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    ]
    role = forms.ChoiceField(choices=PUBLIC_ROLE_CHOICES, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-select' if name == 'role' else 'form-control'


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender', 'mobile_number')
        widgets = {
            'gender': forms.Select(choices=[('', '---'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-select' if name == 'gender' else 'form-control'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'full_name', 'phone', 'address_line1', 'address_line2',
            'city', 'state', 'pincode', 'is_default',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_default':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'