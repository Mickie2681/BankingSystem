from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Diposit, Withdrawal


class DepositForm(forms.ModelForm):
    phone_number = forms.CharField(
        label='Phone Number',max_length=10
    )

    class Meta:
        model = Diposit
        fields = ["phone_number", "amount"]


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.user.account.balance < amount:
            raise forms.ValidationError(
                'You Can Not Withdraw More Than You Balance.'
            )

        return amount
