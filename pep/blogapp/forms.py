from django import forms
from .models import BlogCategory, PostBlog, TagBlog
from django.forms import ModelForm, TextInput

class BlogForm(forms.ModelForm):
    """
    Form to create blogs
    """
    class Meta:
        model = PostBlog
        fields = ['title', 'content', 'image','category','status']


class StatusForm(forms.Form):
    Published  = forms.CharField()
    Unpublished  = forms.CharField()

