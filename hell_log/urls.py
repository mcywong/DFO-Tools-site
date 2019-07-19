from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'hell_log'
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='Sign Up'),
    path('<int:user_id>/create_character/', views.characterCreation, name="Character Creation"),
    path('<int:user_id>/', views.characterList, name="Character List"),
    path('<int:user_id>/<int:character_id>/LogHell', views.logHell, name="Log Hell"),
    path('stats/', views.globalStatistics, name="Global Stats"),
    ## Chart Data view
    path('stats/data/', views.chart_data, name='chart_data'),
    ## bootstrap test page
    path('bootstrap/', TemplateView.as_view(template_name="bootstrap/example.html")),
]
