from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'hell_log'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:account_id>/', views.characterList, name="Character List"),
    path('<int:account_id>/<int:character_id>/LogHell', views.logHell, name="Log Hell"),
    path('stats/', views.globalStatistics, name="Global Stats"),
    ## bootstrap test page
    path('bootstrap/', TemplateView.as_view(template_name="bootstrap/example.html")),
]