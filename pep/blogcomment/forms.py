from django import forms
from django.forms import ModelForm
from .models import BlogCommentModel

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['comment']