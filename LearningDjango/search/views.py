from django.shortcuts import render
from django.db.models import Q
from search.models import Book, titlecase, match_score_sort
from .forms import NewBookForm


# Create your views here.


def index(request):
    return render(request, 'search/index.html')


def advanced_search(request):
    return render(request, 'search/advanced_search.html', {})


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
                for search_term in search_terms:
                    raw_results = Book.objects.filter(title__icontains=search_term)
            elif search_by == "author":
                for search_term in search_terms:
                    raw_results = Book.objects.filter(
                        Q(author_first__icontains=search_term) | Q(author_middle__icontains=search_term) | Q(author_last__icontains=search_term) |
                        Q(author2_first__icontains=search_term) | Q(author2_middle__icontains=search_term) | Q(author2_last__icontains=search_term) |
                        Q(author3_first__icontains=search_term) | Q(author3_middle__icontains=search_term) | Q(author3_last__icontains=search_term))
            elif search_by == "genre":
                for search_term in search_terms:
                    raw_results = Book.objects.filter(
                        Q(genre_1__icontains=search_term) | Q(genre_2__icontains=search_term) |
                        Q(genre_3__icontains=search_term))
            elif search_by == "shelf":
                for search_term in search_terms:
                    raw_results = Book.objects.filter(shelf__icontains=search_term)
            elif search_by == "language":
                for search_term in search_terms:
                    raw_results = Book.objects.filter(language__icontains=search_term)
            elif search_by == "series":
                for search_term in search_terms:
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

    # If POST request comes from advanced search, use the following to filter results
    elif request.POST['search_type'] == "advanced_search":
        # Determine if "match all" or "match any" should be used
        any_all = request.POST['any_all']

        #######
        # Blank strings cause issues for most search areas.
        # An arbitrary string that will return zero matches
        # is needed to allow the search engine to function
        # properly.  As such... YEET
        #######

        # Assign placeholder string for blank fields; otherwise, assign user inputs to variables
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

        # Exclusion variables
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

        # create results list (to be filled later)
        results = []

        # code for "match all" selection -- stricter filtering process
        if any_all == "all":
            # define variables from POST request from advanced search (no placeholder strings (that is, YOINK))
            search_title = request.POST['search_title']
            search_author = request.POST['search_author']
            search_genre = request.POST['search_genre']
            search_language = request.POST['search_language']
            search_shelf = request.POST['search_shelf']

            # create results list based on include filters (before applying exclude filters)
            query = Book.objects.filter(

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

            # add raw results to list "results"
            for i in query:
                if i not in results:
                    results.append(i)

            # collect matching exclusions by given fields (OR operators make this work properly)
            query_exclude = Book.objects.filter(

                Q(title__icontains=search_title_exclude) |

                (Q(author_first__icontains=search_author_exclude) |
                 Q(author_last__icontains=search_author_exclude) |
                 Q(author_middle__icontains=search_author_exclude)) |

                (Q(genre_1__icontains=search_genre_exclude) |
                 Q(genre_2__icontains=search_genre_exclude) |
                 Q(genre_3__icontains=search_genre_exclude)) |

                Q(shelf__icontains=search_shelf_exclude) |

                Q(language__icontains=search_language_exclude)
            )

            # remove matching exclusions from results list
            for i in query_exclude:
                if i in results:
                    results.remove(i)

        # code for "match any" selection, less strict filtering process
        elif any_all == "any":
            # collect matching results by title, author, genre, langauge and shelf
            query = Book.objects.filter(

                Q(title__icontains=search_title) |

                (Q(author_first__icontains=search_author) |
                 Q(author_last__icontains=search_author) |
                 Q(author_middle__icontains=search_author)) |

                (Q(genre_1__icontains=search_genre) |
                 Q(genre_2__icontains=search_genre) |
                 Q(genre_3__icontains=search_genre)) |

                Q(shelf__icontains=search_shelf) |

                Q(language__icontains=search_language)
            )

            # put matching results into results list
            for i in query:
                if i not in results:
                    results.append(i)

            # collect matching exclusions by given fields
            query_exclude = Book.objects.filter(

                Q(title__icontains=search_title_exclude) |

                (Q(author_first__icontains=search_author_exclude) |
                 Q(author_last__icontains=search_author_exclude) |
                 Q(author_middle__icontains=search_author_exclude)) |

                (Q(genre_1__icontains=search_genre_exclude) |
                 Q(genre_2__icontains=search_genre_exclude) |
                 Q(genre_3__icontains=search_genre_exclude)) |

                Q(shelf__icontains=search_shelf_exclude) |

                Q(language__icontains=search_language_exclude)
            )

            # remove matching exclusions from results list
            for i in query_exclude:
                if i in results:
                    results.remove(i)

        # context variable as prescribed by Django
        context = {'results': results}
        return render(request, 'search/results_update.html', context)


def new_book_form(request):
    form = NewBookForm(request.POST or None)
    if form.is_valid():
        new_book = form.save(commit=False)
        dont_clean_data = request.POST.get("dont_clean_data", "false")
        if dont_clean_data == "false":
            title_clean = titlecase(new_book.title)
            author_first_clean = titlecase(new_book.author_first)
            author_last_clean = titlecase(new_book.author_last)
            new_book.title = title_clean
            new_book.author_first = author_first_clean
            new_book.author_last = author_last_clean
        if new_book.genre_1 == "Realistic Fiction":
            new_book.shelf = "1A"
        elif new_book.genre_1 == "Literary Fiction":
            new_book.shelf = "2A"
        elif new_book.genre_1 == "Mystery / Detective Fiction":
            new_book.shelf = "3A"
        elif new_book.genre_1 == "Romance":
            new_book.shelf = "4A"
        elif new_book.genre_1 == "Historical Fiction":
            new_book.shelf = "5A"
        elif new_book.genre_1 == "Thriller / Horror":
            new_book.shelf = "6A"
        elif new_book.genre_1 == "Science Fiction":
            new_book.shelf = "7A"
        elif new_book.genre_1 == "Fantasy":
            new_book.shelf = "8A"
        elif new_book.genre_1 == "Children's Books / Early Readers":
            new_book.shelf = "9A"
        new_book.save()
        context = {'title': new_book.title, 'shelf': new_book.shelf}
        return render(request, 'search/new_book_confirmation.html', context)
    form = NewBookForm()
    context = {'form': form}
    return render(request, 'search/new_book_form.html', context)


def new_book_confirmation(request):
    main_genre = request.POST['genre_1']
    title = request.POST['title']
    shelf = ""
    if main_genre == "Realistic Fiction":
        shelf = "1A"
    elif main_genre == "Literary Fiction":
        shelf = "2A"
    elif main_genre == "Mystery / Detective Fiction":
        shelf = "3A"
    elif main_genre == "Romance":
        shelf = "4A"
    elif main_genre == "Historical Fiction":
        shelf = "5A"
    elif main_genre == "Thriller / Horror":
        shelf = "6A"
    elif main_genre == "Science Fiction":
        shelf = "7A"
    elif main_genre == "Fantasy":
        shelf = "8A"
    elif main_genre == "Children's Books / Early Readers":
        shelf = "9A"
    elif main_genre == "Encyclopedia / General Information":
        shelf = "10A"
    elif main_genre == "Dictionary / Thesaurus":
        shelf = "11A"
    elif main_genre == "Religious":
        shelf = "12A"
    elif main_genre == "Science":
        shelf = "13A"
    elif main_genre == "History":
        shelf = "14A"
    elif main_genre == "Biography / Memoir":
        shelf = "15A"
    elif main_genre == "Self Help":
        shelf = "16A"

    context = {'shelf': shelf, 'title': title}
    return render(request, 'search/new_book_confirmation.html', context)
