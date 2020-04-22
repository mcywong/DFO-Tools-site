from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum

from .logger import HellForm, CharacterForm
from .choices import *
from .models import Character, HellRuns
from django.contrib.auth.decorators import login_required

# Home/Login
def home(request):
    return render(request, 'hell_log/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('hell_log:home'))
    else:
        form = UserCreationForm()
    return render(request, 'hell_log/signup.html', {'form': form})

@login_required(login_url='hell_log:login')
def characterCreation(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        character = Character(account = user)
        form = CharacterForm(request.POST, instance=character)
        form.save()
        if form.is_valid():
            return HttpResponseRedirect(reverse('hell_log:Character List', kwargs={'user_id':user_id}))
    else:
        form = CharacterForm()

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'hell_log/characterCreation.html', context)

@login_required(login_url='hell_log:login')
def characterList(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    character_set = list(Character.objects.filter(account=user_id).order_by('id'))
    context = {
        'character_set':character_set,
        'user': user,
    }
    return render(request, "hell_log/characterList.html", context)

@login_required(login_url='hell_log:login')
def logHell(request, user_id, character_id):
    user = get_object_or_404(User, pk=user_id)
    character = get_object_or_404(Character, pk=character_id)
    if request.method == 'POST':
        hellRun = HellRuns(character = character)
        form = HellForm(request.POST, instance=hellRun)
        form.save()
        if form.is_valid():
            # for now direct to GLOBAL statistics
            return HttpResponseRedirect(reverse('hell_log:Global Stats'))
    else:
        form = HellForm()
    
    context = {
        'form': form,
        "user": user,
        'character': character,
    }
    return render(request, "hell_log/logger.html", context)


#public graph views
def chart_data(request):
    wisdom_rates = getDropRates(GUIDE_OF_WISDOM)
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Global Drop Rates in all Hell Runs'},
        'xAxis': {'categories': ['Epic Gear', 'Stone Box', 'Epic Souls']},
        'yAxis': {'title':{'text': 'Drop Rates (%)'}},
        'plotOptions':{
            'column':{
                'dataLabels':{'enabled': 'true'}
            }
        },
        'series': [{
            'name': "Guide of Wisdom",
            'data': wisdom_rates,
        }]
    }

    return JsonResponse(chart)

def globalStatistics(request):
    return render(request,'hell_log/globalStats.html')


def getDropRates(Hell_Type):
    hell_runs = HellRuns.objects.filter(HellType=Hell_Type).aggregate(total_runs=Sum('Runs'),)
    runs = hell_runs['total_runs']
    if runs is None or runs == 0:
        return [0, 0, 0,]

    drop_query = HellRuns.objects.filter(HellType=Hell_Type).aggregate(
        total_drops=Sum('EpicDrops'),
        total_boxes=Sum('StoneBox'),
        total_souls=Sum('EpicSoul'),
    )
    drop_list = [
        drop_query['total_drops'],
        drop_query['total_boxes'],
        drop_query['total_souls'],
    ]

    return [float('%.3f'%(v/runs*100)) for v in drop_list]
