from django import forms
from .models import Issue

# issue app 내용
class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'keyword',
            'title',
            'context',
            'link1',
            'link2',
            'link3',
        ]