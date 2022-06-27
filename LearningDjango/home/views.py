from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.


def index(request):
    template = loader.get_template('home/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def search_redirect(request):
    return redirect('search:index')

    # context = {}
    # return render(request, 'home/index.html', context)
