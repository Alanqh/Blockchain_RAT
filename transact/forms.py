from django import forms

from records.models import TransactionRecords


class TransactForm(forms.ModelForm):
    class Meta:
        model = TransactionRecords
        fields = ['TransactionAmount']
        labels = {
            'AchievementID': '成果ID',
            'Seller': '出售方',
            'Buyer': '购买方',
            'TransactionAmount': '交易金额',
        }


class ConfirmTransactionForm(forms.Form):
    CHOICES = [(True, '同意交易'), (False, '不同意交易')]
    agree_to_transact = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


from django import forms


class SecondTransactForm(forms.Form):
    new_price = forms.DecimalField(max_digits=6, decimal_places=2, label='设置一个新的价格：')
