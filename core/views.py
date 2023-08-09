from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

@login_required(login_url="/login/")
def home(request):
    from NOC.models import Kit

    kits_dict = {}
    kits = Kit.objects.all()
    for kit in kits:
        if kit.meraki_device:
            kits_dict[kit.site_id] = kit.site.description

    return render(request, 'page-landing-app.html', {"kits":kits_dict})

def kitSearcher(request):
    from NOC.models import Kit
    from django.http import JsonResponse
    term = request.GET.get('term', '')
    kits = Kit.objects.filter(site__description__contains=term)
    results = [{'id': kit.site._id, 'text': kit.site.description} for kit in kits]
    if results: return JsonResponse(results, safe=False)


def charttest(request):
    return render(request, 'noc/piechart.html')

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # print(request.path)
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)

        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))