from enum import Enum

from django import forms
from django.utils.translation import ugettext_lazy as _


CURRENCIES = (
    ("EUR", "EUR"),
    ("RUB", "RUB"),
    ("USD", "USD"),
    ("GBP", "GBP"),
)


class RetrieveForm(forms.Form):
    date = forms.DateField(
        label="Date",
        required=True,
        widget=forms.SelectDateWidget()
    )


class ExchangeForm(forms.Form):
    currency = forms.ChoiceField(
        label="Currency code",
        choices=sorted(CURRENCIES),
        widget=forms.RadioSelect)
