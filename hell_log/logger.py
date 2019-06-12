# Form class that will generate the html form for the hell logger

from django.forms import ModelForm
from .models import HellRuns

class HellForm(ModelForm):
    class Meta:
        model = HellRuns
        exclude = ['character', 'Date']
