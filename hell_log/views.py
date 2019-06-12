from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum

from .logger import HellForm
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

def globalStatistics(request):
    totalRuns = HellRuns.objects.aggregate(Sum('Runs'))
    totalDrops = HellRuns.objects.aggregate(Sum('EpicDrops'))
    context = {
        'total_runs': totalRuns['Runs__sum'],
        'total_drops': totalDrops['EpicDrops__sum'],
    }
    return render(request,'hell_log/globalStats.html', context)


