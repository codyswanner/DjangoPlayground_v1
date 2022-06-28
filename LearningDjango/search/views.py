from django.shortcuts import render
from django.db.models import Q
from search.models import Books

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
        results = Books.objects.all()
        search_by = "*"
    else:
        if search_by == "all":
            results = Books.objects.filter(
                Q(author_first__icontains=search_term) |
                Q(author_last__icontains=search_term) |
                Q(author_middle__icontains=search_term) |
                Q(title__icontains=search_term) |
                Q(genre_1__icontains=search_term) |
                Q(genre_2__icontains=search_term) |
                Q(genre_3__icontains=search_term) |
                Q(shelf__icontains=search_term) |
                Q(language__icontains=search_term))
        elif search_by == "title":
            results = Books.objects.filter(title__icontains=search_term)
        elif search_by == "author":
            results = Books.objects.filter(Q(author_first__icontains=search_term) | Q(author_last__icontains=search_term))
        elif search_by == "genre":
            results = Books.objects.filter(Q(genre_1__icontains=search_term) | Q(genre_2__icontains=search_term) | Q(genre_3__icontains=search_term))
        elif search_by == "shelf":
            results = Books.objects.filter(shelf__icontains=search_term)
        elif search_by == "language":
            results = Books.objects.filter(language__contains=search_term)
        # Add else statement that brings up error page
    context = {'search_term': search_term,
               'results': results,
               'search_by': search_by,
               }
    return render(request, 'search/results.html', context)
