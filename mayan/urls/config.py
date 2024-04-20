from django.shortcuts import render, redirect
from mayan.apps.documents.models.document_models import Config

def config_list(request):
    configs = Config.objects.all()[::-1]
    return render(request, 'config/config_list.html', {'configs': configs})

def create_config(request):
    configs = Config.objects.all()[::-1]
    if request.method == 'POST':
        last_length = request.POST.get('last_length')
        Config.objects.create(last_length=last_length)
        return redirect('config_list')
    return render(request, 'config/create_config.html', {'l_data':configs[0].last_length})
