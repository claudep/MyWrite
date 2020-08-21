from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from tinymce.models import HTMLField
from django.utils import timezone
import datetime
class Article(models.Model):
    title = models.CharField('כותרת',max_length=100)
    author = models.CharField('יוצר',max_length=50, default="first name")
    pub_date = models.DateTimeField('תאריך פרסום', auto_now_add=True)
    text = HTMLField('גוף',max_length=4000)
    votes = models.IntegerField('הצבעות' ,default=0)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def get_queryset(self):
        """Return the last five published questions."""
        return Article.objects.order_by('-pub_date')[:5]

# class Vote(models.Model):
#     user = models.ForeignKey(User)
#     article = models.ForeignKey(Article)

class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("למשתמש חייב להיות דואר אלקטרוני")
        if not first_name or not last_name :
            raise ValueError("למשתמש חייב להיות שם פרטי ושם משפחה ")

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="דואר אלקטרוני", max_length=60, unique=True)
    first_name = models.CharField(verbose_name="שם פרטי" ,max_length=30)
    last_name = models.CharField(verbose_name="שם משפחה" ,max_length=30)
    date_joined = models.DateTimeField(verbose_name="תאריך הצטרפות" ,auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="כניסה אחרונה למערכת", auto_now=True)
    is_admin = models.BooleanField(verbose_name="מנהל" ,default=False)
    is_active = models.BooleanField(verbose_name="פעיל" ,default=False)
    is_staff = models.BooleanField(verbose_name="עובד", default=False)
    is_superuser = models.BooleanField(verbose_name="משתמש עליון" ,default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name + " " + self.last_name + ", " + self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True