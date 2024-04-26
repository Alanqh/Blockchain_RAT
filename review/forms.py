from django import forms

class ReviewForm(forms.Form):
    REVIEW_CHOICES = [
        ('1', '通过'),
        ('2', '未通过'),
    ]
    review_result = forms.ChoiceField(choices=REVIEW_CHOICES, widget=forms.RadioSelect, label='审核结果')
    review_comments = forms.CharField(required=False, widget=forms.Textarea, label='审核意见')