from django import forms
from .models import Address


class addressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'street_address', 'city', 'state', 'zip_code', 'country', 'phone']
        widgets = {
            'country': forms.Select(choices=[
                ('IN', 'India'),
                ('US', 'United States'),
                ('CA', 'Canada'),
                ('GB', 'United Kingdom'),
                ('AU', 'Australia')
            ],
            attrs={'class': 'form-control'}
            ),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'frist_name': 'First Name',
            'last_name': 'Last Name',
            'street_address': 'Street Address',
            'city': 'City',
            'state': 'State',
            'zip_code': 'ZIP/Postal Code',
            'country': 'Country',
            'phone': 'Phone Number',
        }