from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import DepositForm, WithdrawalForm

from django.shortcuts import render
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse, JsonResponse

cl = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = 'https://api.darajambili.com/b2c/result'


def oauth__success(request):
    r = cl.access_token()
    return JsonResponse(r, safe=False)


@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.save()

            phone_number = form.cleaned_data['phone_number']

            amount = int(form.cleaned_data['amount'])
            account_reference = "Kenya International Bank"
            transaction_desc = 'STK Push Description'

            r = cl.stk_push(phone_number, amount, account_reference, transaction_desc, stk_push_callback_url)

            if r.response_code == "0":

                deposit.stk_push_status = True
                deposit.save()

                deposit.user.account.balance += deposit.amount
                deposit.user.account.save()

                messages.success(request, 'You have deposited {} . STK Push successful.'
                                 .format(deposit.amount))
            else:

                messages.error(request, f'STK Push failed: {r.response_description}')

            return redirect("core:home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


@login_required()
def withdrawal_view(request):
    form = WithdrawalForm(request.POST or None, user=request.user)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.save()
        # subtracts users withdrawal from balance.
        withdrawal.user.account.balance -= withdrawal.amount
        withdrawal.user.account.save()

        messages.success(
            request, 'You Have Withdrawn {} $.'.format(withdrawal.amount)
        )
        return redirect("core:home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "transactions/form.html", context)
