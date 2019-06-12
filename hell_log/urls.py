from django.urls import path

from . import views

app_name = 'hell_log'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:account_id>/', views.characterList, name="Character List"),
    path('<int:account_id>/<int:character_id>/LogHell', views.logHell, name="Log Hell"),
    path('stats/', views.globalStatistics, name="Global Stats"),
]