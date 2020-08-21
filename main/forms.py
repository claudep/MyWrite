from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, Article
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
import datetime
class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name', 'email')

class ArticleCreationForm(forms.ModelForm): 
    # specify the name of model to use 
    # text = forms.Textarea(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta: 
        model = Article 
        fields = '__all__'
        # widgets = {
        #     'text': forms.Textarea(attrs={'rows':18, 'cols':130}),
        # }
        exclude = ['votes', 'author']