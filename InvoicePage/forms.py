from django import forms
from django.forms import formset_factory

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class DetailsForm(forms.Form):
    sortCode = forms.CharField()
    phoneNumber = forms.IntegerField()
    address = forms.CharField()
    company = forms.CharField()
    bankDetail = forms.CharField()

class surgeryForm(forms.Form):
    surgeryChosen = forms.ChoiceField(
        choices=[
            ("Pondtail Surgery", "Pondtail Surgery"),
            ("Shirley Medical Centre", "Shirley Medical Centre"),
            ("Bishopford Road Surgery", "Bishopford Road Surgery"),
            ("Thornton Road Medical Centre", "Thornton Road Medical Centre")
        ],
        widget=forms.Select,
        label="Choose a surgery:",
        required=True  # This field is required
    )
    hourlyRate = forms.IntegerField(
        required=True  # This field is required
    )


class calendarForm(forms.Form):
    datesChosen = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}))
    timeChosenStart = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    hoursPerDay = forms.IntegerField()
