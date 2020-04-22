# Form class that will generate the html form for the hell logger

from django.forms import ModelForm
from .models import HellRuns, Character

class HellForm(ModelForm):
    class Meta:
        model = HellRuns
        exclude = ['character', 'Date']
        labels = {
            'HellType': 'Hell Type',
            'Runs': 'Hell Runs Done',
            'EpicDrops': 'Epic Gears Dropped',
            'StoneBox': 'Time Guide Stone Boxes',
            'EpicSoul': 'Epic Souls',
        }
    
    def __init__(self, *args, **kwargs):
        super(HellForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        exclude= ['account']
    
    def __init__(self, *args, **kwargs):
        super(CharacterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'