from django.shortcuts import render
from django.db.models import Q
from search.models import Book,  match_score_sort


def search_results(request):
    if request.POST['search_type'] == "default_search":
        search_by = request.POST['search_by']
        search_term = request.POST['search_term']
        # Using * overrides search_by and shows all data (also displays "searched * by *")
        if search_term == "*":
            results = Book.objects.all()
            search_by = "*"
        else:
            raw_input = request.POST['search_term']
            search_terms = []
            raw_results = []
            results = []
            genre_options = [
                "realistic fiction",
                "literary fiction",
                "historical fiction",
                "mystery",
                "detective fiction",
                "romance",
                "historical fiction",
                "thriller",
                "horror",
                "science fiction",
                "fantasy",
                "children's books",
                "childrens books",
                "early readers"
            ]
            for genre in genre_options:
                if genre in raw_input.lower():
                    raw_input = raw_input.lower().replace(genre, "")
                    search_terms.append(genre)
            for x in raw_input.split():
                if x.lower() == "the" or x.lower() == "at" or x.lower() == "of" or x.lower() == "and":
                    pass
                else:
                    search_terms.append(x)
            if search_by == "all":
                for search_term in search_terms:
                    raw_results = Book.objects.filter(
                        Q(author_first__icontains=search_term) |
                        Q(author_last__icontains=search_term) |
                        Q(author_middle__icontains=search_term) |
                        Q(title__icontains=search_term) |
                        Q(genre_1__icontains=search_term) |
                        Q(genre_2__icontains=search_term) |
                        Q(genre_3__icontains=search_term) |
                        Q(shelf__icontains=search_term) |
                        Q(language__icontains=search_term) |
                        Q(series__icontains=search_term))
            elif search_by == "title":
                raw_results = Book.objects.filter(title__icontains=search_term)
            elif search_by == "author":
                raw_results = Book.objects.filter(
                    Q(author_first__icontains=search_term) | Q(author_middle__icontains=search_term) | Q(author_last__icontains=search_term) |
                    Q(author2_first__icontains=search_term) | Q(author2_middle__icontains=search_term) | Q(author2_last__icontains=search_term) |
                    Q(author3_first__icontains=search_term) | Q(author3_middle__icontains=search_term) | Q(author3_last__icontains=search_term))
            elif search_by == "genre":
                raw_results = Book.objects.filter(
                    Q(genre_1__icontains=search_term) | Q(genre_2__icontains=search_term) | Q(
                        genre_3__icontains=search_term))
            elif search_by == "shelf":
                raw_results = Book.objects.filter(shelf__icontains=search_term)
            elif search_by == "language":
                raw_results = Book.objects.filter(language__icontains=search_term)
            elif search_by == "series":
                raw_results = Book.objects.filter(series__icontains=search_term)
            # Add else statement that brings up error page
            for result in raw_results:
                if result not in results:
                    results.append(result)
                else:
                    # if you've reached this block of code, congrats, you're already in the list and now
                    # your match score will be increased!  "emi" stands for "existing match index" and is used
                    # to increase the match score for the correct match.
                    emi = results.index(result)
                    results[emi].match_score += 1
                    print(results[emi].match_score)
            results.sort(reverse=True, key=match_score_sort)
        context = {'search_term': search_term,
                   'results': results,
                   'search_by': search_by,
                   }
        return render(request, 'search/results_update.html', context)
