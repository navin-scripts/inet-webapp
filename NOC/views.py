from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.core.serializers.base import Serializer
from .models import Kit, UnifiSite


def unifi(request):
    return render(request, 'production/noc/page-support.html')

def fastl2lookup(request):
    return render(request, 'production/noc/page-support.html')

def unifilookup(request):
    from NOC.models import UnifiDevice
    try:
        device = UnifiDevice.objects.filter(mac=request.POST.get('unifi_mac')).select_related('site_id')
    except:
        device = []
    # for d in device: print()
    return render(request, 'production/noc/unifi/devicepage.html', {'device':device})