from django import forms

from records.models import TransactionRecords


class TransactForm(forms.ModelForm):
    class Meta:
        model = TransactionRecords
        fields = ['TransactionAmount']
        labels = {
            'AchievementID': '成果ID',
            'Seller':'出售方',
            'Buyer': '购买方',
            'TransactionAmount': '交易金额',
        }


class ConfirmTransactionForm(forms.Form):
    CHOICES = [(True, '同意交易'), (False, '不同意进行交易')]
    agree_to_transact = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)