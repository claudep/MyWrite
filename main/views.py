from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import logout, authenticate, login
from django.views.generic.edit import CreateView
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q
import datetime

from .forms import AccountCreationForm, ArticleCreationForm
from .models import Article, Account
from .token import account_activation_token

def index(request):
    latest_article_list = Article.objects.order_by('-votes')[:5]
    context = {'latest_article_list': latest_article_list}
    return render(request, 'main/index.html', context)


class DetailView(generic.DetailView):
    model = Article
    template_name = 'main/article.html'

# @login_required
def vote(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.votes += 1
    article.save()
    return JsonResponse(data = {"vote": "Voted! Thank you for the vote."})

def write(request):
    if request.user.is_authenticated:
        context = {} 
        # create object of form 
        form = ArticleCreationForm(request.POST) 
        # check if form data is valid 
        if request.method == "POST":
            if form.is_valid(): 
                article = form.save(commit=False) 
                article.author = request.user.first_name+' '+request.user.last_name # the user must be logged in for this.
                article.save()
            # save the form data to model 
    
        context['form']= form 
        return render(request, "main/article_creation_form.html", context) 
    else:
        return HttpResponse("calitol")

def register(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            print(get_current_site(request))
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('main/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = form.cleaned_data.get('email')
            email_message = EmailMessage(
                        mail_subject, message, to=[email]
            )
            email_message.send()
            messages.add_message(request, messages.INFO, 'שלחנו הודעה לדואר האלקטרוני שלך בה נמצא קישור להפעלת החשבון.')
            login(request, user)
            return HttpResponse("Please confirm your email address")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = AccountCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

class SearchResultsView(ListView):
    model = Article
    template_name = 'main/search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        return Article.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )