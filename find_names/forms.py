from django import forms

class DateForm(forms.Form):
    view_date = forms.DateField(label='Date to find schedule')