from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Sum

from .logger import HellForm
from .choices import HARLEM_HELL, SKY_RIFT, CELESTIAL_RIFT
from .models import Account, Character, HellRuns

# Create your views here.
def home(request):
    latest_account_list = Account.objects.order_by('id')
    context = {
        'latest_account_list': latest_account_list,
    }
    return render(request, 'hell_log/home.html',context)

def characterList(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, "hell_log/characterList.html", {"account": account})

def logHell(request, account_id, character_id):
    account = get_object_or_404(Account, pk=account_id)
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
        "account": account,
        'character': character,
    }
    return render(request, "hell_log/logger.html", context)

def chart_data(request):
    harlem_rates = getDropRates(HARLEM_HELL)
    sky_rates = getDropRates(SKY_RIFT)
    celestial_rates = getDropRates(CELESTIAL_RIFT)
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Global Drop Rates in all Hell Runs'},
        'xAxis': {'categories': ['Epic Gear', 'Hell Orb', 'Stone Box', 'Epic Souls']},
        'series': [{
            'name': 'Harlem Hell',
            'data': harlem_rates
        }, {
            'name': 'Sky Rift',
            'data': sky_rates
        }, {
            'name': 'Celestial Rift',
            'data': celestial_rates
        }]
    }

    return JsonResponse(chart)

def globalStatistics(request):
    return render(request,'hell_log/globalStats.html')


def getDropRates(Hell_Type):
    hell_runs = HellRuns.objects.filter(HellType=Hell_Type).aggregate(total_runs=Sum('Runs'),)
    runs = hell_runs['total_runs']
    if runs is None or runs == 0:
        return [0, 0, 0, 0]

    drop_query = HellRuns.objects.filter(HellType=Hell_Type).aggregate(
        total_drops=Sum('EpicDrops'),
        total_orbs=Sum('HellOrb'),
        total_boxes=Sum('StoneBox'),
        total_souls=Sum('EpicSoul'),
    )
    drop_list = [
        drop_query['total_drops'],
        drop_query['total_orbs'],
        drop_query['total_boxes'],
        drop_query['total_souls'],
    ]

    return [v/runs for v in drop_list]
