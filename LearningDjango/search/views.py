from django.shortcuts import render
from django.db.models import Q
from search.models import Stuff

# Create your views here.

#
# def index(request):
#     return HttpResponse("Here's the search page! (Search bar forthcoming)")


def index(request):
    return render(request, 'search/index.html')


def search_results(request):
    search_by = request.POST['search_by']
    search_term = request.POST['search_term']
    # empty results set here isn't necessary, just makes PyCharm warning shut up
    results = []
    # Using * overrides search_by and shows all data (also displays "searched * by *")
    if search_term == "*":
        results = Stuff.objects.all()
        search_by = "*"
    else:
        if search_by == "all":
            results = Stuff.objects.filter(Q(color__contains=search_term) | Q(name__contains=search_term))
        elif search_by == "name":
            results = Stuff.objects.filter(name__contains=search_term)
        elif search_by == "color":
            results = Stuff.objects.filter(color__contains=search_term)
    return render(request, 'search/results.html', {'search_term': search_term, 'results': results, 'search_by': search_by})
