# Generated by Django 3.1 on 2020-08-19 12:16

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='דואר אלקטרוני')),
                ('first_name', models.CharField(max_length=30, verbose_name='שם פרטי')),
                ('last_name', models.CharField(max_length=30, verbose_name='שם משפחה')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='תאריך הצטרפות')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='כניסה אחרונה למערכת')),
                ('is_admin', models.BooleanField(default=False, verbose_name='מנהל')),
                ('is_active', models.BooleanField(default=False, verbose_name='פעיל')),
                ('is_staff', models.BooleanField(default=False, verbose_name='עובד')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='משתמש עליון')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='כותרת')),
                ('author', models.CharField(default='first name', max_length=50, verbose_name='יוצר')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='תאריך פרסום')),
                ('text', tinymce.models.HTMLField(max_length=4000, verbose_name='גוף')),
                ('votes', models.IntegerField(default=0, verbose_name='הצבעות')),
            ],
        ),
    ]