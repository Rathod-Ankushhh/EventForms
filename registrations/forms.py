
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Event


class RegistrationForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )

    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    phone = forms.CharField(
        max_length=10,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )

    college = forms.CharField(
        max_length=200,
        required=True,
        label="College Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your college name'
        })
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()

        if len(name) < 3:
            raise ValidationError(
                "Name must contain at least 3 characters."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:
            raise ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone

    def clean_college(self):
        college = self.cleaned_data['college'].strip()

        if not college:
            raise ValidationError(
                "College name should not be empty."
            )

        return college


class OrganizerSignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create password'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'name',
            'description',
            'date',
            'venue',
            'available_seats'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event name'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your event'
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'venue': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event venue'
            }),

            'available_seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Number of seats'
            })
        }
