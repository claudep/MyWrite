from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from tinymce.models import HTMLField

from .models import Article, Account

# class ArticleAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'text']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    ordering = ['pub_date']
    readonly_fields = ('author','pub_date')
    search_fields = ['title', 'author']
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size':'60'})},
    #     HTMLField: {'widget': HTMLField({'rows':18, 'cols':130})},
    # }

class AccountAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name']
    ordering = ['date_joined']
    readonly_fields = ('date_joined', 'last_login')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Account, AccountAdmin)