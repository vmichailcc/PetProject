from django import forms
from .models import ProductComment


class AddProductComment(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['text']

