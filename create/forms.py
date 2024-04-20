from django import forms
from .models import ResearchResult, ResearchFile


class ResearchResultForm(forms.ModelForm):
    class Meta:
        model = ResearchResult
        fields = ['Title', 'Abstract', 'Price', 'Keywords', 'AchievementType']


class ResearchFileForm(forms.ModelForm):
    class Meta:
        model = ResearchFile
        fields = ['file']
