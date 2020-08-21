from django.urls import path, include
from django.conf.urls import url

from . import views
from .views import SearchResultsView
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path("register/", views.register, name="register"),
    path('<int:article_id>/vote/', views.vote, name='vote'),
    path('write/', views.write, name='write'),
    path('tinymce/', include('tinymce.urls')),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        views.activate, name='activate'),
]