from django import forms
from .models import Balance, Transaction


class BalanceForm(forms.ModelForm):
	model = Balance
	email = forms.CharField(label='email', max_length=30)
	total_amount = forms.DecimalField(
		label='amount', max_digits=9, decimal_places=2)
	currency = forms.CharField(label='currency', max_length=3)


class BalanceUploadForm(forms.ModelForm):
	class Meta:
		model = Balance

		exclude = ['user',]