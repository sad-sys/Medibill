from django import forms
from django.forms import formset_factory

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class surgeryForm(forms.Form):
    surgeryChosen = forms.ChoiceField(
        choices=[
            ("None", "None"),
            ("Pondtail Surgery", "Pondtail Surgery"),
            ("Shirley Medical Centre", "Shirley Medical Centre"),
            ("Bishopford Road Surgery", "Bishopford Road Surgery"),
            ("Thornton Road Medical Centre", "Thornton Road Medical Centre")
        ],
        widget=forms.Select,
        label="Choose a surgery:"
    )

class calendarForm(forms.Form):
    datesChosen = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}))
    timeChosenStart = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    hoursPerDay = forms.IntegerField()
