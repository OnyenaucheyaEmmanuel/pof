from django import forms
from .models import FormEntry

class FormEntryForm(forms.ModelForm):
    class Meta:
        model = FormEntry
        fields = ['name', 'email', 'phone', 'amount', 'bank_name', 'start_date', 'expiration_days']
