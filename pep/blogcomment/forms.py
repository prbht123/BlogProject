from django import forms
from django.forms import ModelForm
from .models import BlogCommentModel, BlogRatingModel

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['comment']


class BlogRatingForm(forms.ModelForm):
    class Meta:
        model = BlogRatingModel
        fields = ['rating']