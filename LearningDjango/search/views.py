from django.shortcuts import render
from django.db.models import Q
from search.models import Books


# Create your views here.

#
# def index(request):
#     return HttpResponse("Here's the search page! (Search bar forthcoming)")


def index(request):
    return render(request, 'search/index.html')


def advanced_search(request):
    return render(request, 'search/advanced_search.html', {})


def search_results(request):
    if request.POST['search_type'] == "default_search":
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
                results = Books.objects.filter(
                    Q(author_first__icontains=search_term) | Q(author_last__icontains=search_term))
            elif search_by == "genre":
                results = Books.objects.filter(
                    Q(genre_1__icontains=search_term) | Q(genre_2__icontains=search_term) | Q(
                        genre_3__icontains=search_term))
            elif search_by == "shelf":
                results = Books.objects.filter(shelf__icontains=search_term)
            elif search_by == "language":
                results = Books.objects.filter(language__contains=search_term)
            # Add else statement that brings up error page
        context = {'search_term': search_term,
                   'results': results,
                   'search_by': search_by,
                   }
        return render(request, 'search/results_update.html', context)
    elif request.POST['search_type'] == "advanced_search":
        any_all = request.POST['any_all']
        if request.POST['search_title'] != "":
            search_title = request.POST['search_title']
        else:
            search_title = "YEET"
        if request.POST['search_author'] != "":
            search_author = request.POST['search_author']
        else:
            search_author = "YEET"
        if request.POST['search_genre'] != "":
            search_genre = request.POST['search_genre']
        else:
            search_genre = "YEET"
        if request.POST['search_language'] != "":
            search_language = request.POST['search_language']
        else:
            search_language = "YEET"
        if request.POST['search_shelf'] != "":
            search_shelf = request.POST['search_shelf']
        else:
            search_shelf = "YEET"

        if request.POST['search_title_exclude'] != "":
            search_title_exclude = request.POST['search_title_exclude']
        else:
            search_title_exclude = "YEET"
        if request.POST['search_author_exclude'] != "":
            search_author_exclude = request.POST['search_author_exclude']
        else:
            search_author_exclude = "YEET"
        if request.POST['search_genre_exclude'] != "":
            search_genre_exclude = request.POST['search_genre_exclude']
        else:
            search_genre_exclude = "YEET"
        if request.POST['search_language_exclude'] != "":
            search_language_exclude = request.POST['search_language_exclude']
        else:
            search_language_exclude = "YEET"
        if request.POST['search_shelf_exclude'] != "":
            search_shelf_exclude = request.POST['search_shelf_exclude']
        else:
            search_shelf_exclude = "YEET"

        results = []
        if any_all == "all":
            # define variables from POST request from advanced search
            search_title = request.POST['search_title']
            search_author = request.POST['search_author']
            search_genre = request.POST['search_genre']
            search_language = request.POST['search_language']
            search_shelf = request.POST['search_shelf']

            # create results list based on include filters (before exclude filters)
            query = Books.objects.filter(

                Q(title__icontains=search_title) &

                (Q(author_first__icontains=search_author) |
                 Q(author_last__icontains=search_author) |
                 Q(author_middle__icontains=search_author)) &

                (Q(genre_1__icontains=search_genre) |
                 Q(genre_2__icontains=search_genre) |
                 Q(genre_3__icontains=search_genre)) &

                Q(shelf__icontains=search_shelf) &

                Q(language__icontains=search_language)
            )

            for i in query:
                if i not in results:
                    results.append(i)

            # collect matching exclusions by given fields
            title_results_exclude = Books.objects.filter(title__icontains=search_title_exclude)
            author_results_exclude = Books.objects.filter(
                Q(author_first__icontains=search_author_exclude) | Q(
                    author_last__icontains=search_author_exclude) | Q(
                    author_middle__icontains=search_author_exclude))
            genre_results_exclude = Books.objects.filter(
                Q(genre_1__icontains=search_genre_exclude) | Q(genre_2__icontains=search_genre_exclude) | Q(
                    genre_3__icontains=search_genre_exclude))
            language_results_exclude = Books.objects.filter(language__icontains=search_language_exclude)
            shelf_results_exclude = Books.objects.filter(shelf__icontains=search_shelf_exclude)

            # remove matching exclusions from results list
            for i in title_results_exclude:
                if i in results:
                    results.remove(i)
            for i in author_results_exclude:
                if i in results:
                    results.remove(i)
            for i in genre_results_exclude:
                if i in results:
                    results.remove(i)
            for i in language_results_exclude:
                if i in results:
                    results.remove(i)
            for i in shelf_results_exclude:
                if i in results:
                    results.remove(i)

            # apply exception filters


            # # collect matching exclusions by given fields
            # title_results_exclude = Books.objects.filter(title__icontains=search_title_exclude)
            # author_results_exclude = Books.objects.filter(
            #     Q(author_first__icontains=search_author_exclude) | Q(author_last__icontains=search_author_exclude) | Q(
            #         author_middle__icontains=search_author_exclude))
            # genre_results_exclude = Books.objects.filter(
            #     Q(genre_1__icontains=search_genre_exclude) | Q(genre_2__icontains=search_genre_exclude) | Q(
            #         genre_3__icontains=search_genre_exclude))
            # language_results_exclude = Books.objects.filter(language__icontains=search_language_exclude)
            # shelf_results_exclude = Books.objects.filter(shelf__icontains=search_shelf_exclude)
            #
            # # remove matching exclusions from results list
            # for i in title_results_exclude:
            #     if i in results:
            #         results.remove(i)
            # for i in author_results_exclude:
            #     if i in results:
            #         results.remove(i)
            # for i in genre_results_exclude:
            #     if i in results:
            #         results.remove(i)
            # for i in language_results_exclude:
            #     if i in results:
            #         results.remove(i)
            # for i in shelf_results_exclude:
            #     if i in results:
            #         results.remove(i)

        elif any_all == "any":
            # collect matching results by title, author, genre, langauge and shelf
            title_results = Books.objects.filter(title__icontains=search_title)
            author_results = Books.objects.filter(
                Q(author_first__icontains=search_author) | Q(author_last__icontains=search_author) | Q(
                    author_middle__icontains=search_author))
            genre_results = Books.objects.filter(
                Q(genre_1__icontains=search_genre) | Q(genre_2__icontains=search_genre) | Q(
                    genre_3__icontains=search_genre))
            language_results = Books.objects.filter(language__icontains=search_language)
            shelf_results = Books.objects.filter(shelf__icontains=search_shelf)

            # put matching results into results list
            for i in title_results:
                results.append(i)
            for i in author_results:
                if i not in results:
                    results.append(i)
            for i in genre_results:
                if i not in results:
                    results.append(i)
            for i in language_results:
                if i not in results:
                    results.append(i)
            for i in shelf_results:
                if i not in results:
                    results.append(i)

            # collect matching exclusions by given fields
            title_results_exclude = Books.objects.filter(title__icontains=search_title_exclude)
            author_results_exclude = Books.objects.filter(
                Q(author_first__icontains=search_author_exclude) | Q(
                    author_last__icontains=search_author_exclude) | Q(
                    author_middle__icontains=search_author_exclude))
            genre_results_exclude = Books.objects.filter(
                Q(genre_1__icontains=search_genre_exclude) | Q(genre_2__icontains=search_genre_exclude) | Q(
                    genre_3__icontains=search_genre_exclude))
            language_results_exclude = Books.objects.filter(language__icontains=search_language_exclude)
            shelf_results_exclude = Books.objects.filter(shelf__icontains=search_shelf_exclude)

            # remove matching exclusions from results list
            for i in title_results_exclude:
                if i in results:
                    results.remove(i)
            for i in author_results_exclude:
                if i in results:
                    results.remove(i)
            for i in genre_results_exclude:
                if i in results:
                    results.remove(i)
            for i in language_results_exclude:
                if i in results:
                    results.remove(i)
            for i in shelf_results_exclude:
                if i in results:
                    results.remove(i)
        context = {'results': results}
        return render(request, 'search/results_update.html', context)
