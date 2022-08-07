from django.db import models
import re


# Create your models here.

# This function sorts which words in titles should be capitalized and returns them appropriately.
# To be used with titlecase function defined below
def cap(x):
    if x.group('exceptions'):
        return x.group('exceptions')
    else:
        return x.group().capitalize()


# This function takes in and returns input strings (such as titles, authors, etc.) to capitalize them appropriately.
def titlecase(s):
    reg_exp = r"(?P<exceptions> and| the| of| for| in| at| to| an| by| on| that| but| yet| so| nor| or| as| a )|[a-zA-ZÀ-ÿ]+('[A-Za-zÀ-ÿ]+)?"
    return re.sub(reg_exp, cap, s)


# This function works in views.py, function search_results.
# It scores results for relevance sorting based on how many times a result matches with search terms.
def compile_results(raw_results, results_list):
    for result in raw_results:
        if result not in results_list:
            results_list.append(result)
            result.match_score = 0
            print("New result: " + result.title)
        else:
            # if you've reached this block of code, congrats, you're already in the list and now
            # your match score will be increased!  "emi" stands for "existing match index" and is used
            # to increase the match score for the correct match.
            emi = results_list.index(result)
            results_list[emi].match_score += 1
            print("Score updated for " + result.title + " to " + str(results_list[emi].match_score))


def match_score_sort(result):
    return result.match_score


class Book(models.Model):
    title = models.CharField(max_length=70, null=False)
    author_first = models.CharField(max_length=30, null=False)
    author_middle = models.CharField(max_length=30, null=True, blank=True)
    author_last = models.CharField(max_length=30, null=False)
    genre_choices_abridged = [
        ("Realistic Fiction", "Realistic Fiction"),
        ("Literary Fiction", "Literary Fiction"),
        ("Mystery / Detective Fiction", "Mystery / Detective Fiction"),
        ("Romance", "Romance"),
        ("Historical Fiction", "Historical Fiction"),
        ("Thriller / Horror", "Thriller / Horror"),
        ("Science Fiction", "Science Fiction"),
        ("Fantasy", "Fantasy"),
        ("Children's Books / Early Readers", "Children's Books / Early Readers"),
        ("Encyclopedia / General Information", "Encyclopedia / General Information"),
        ("Dictionary / Thesaurus", "Dictionary / Thesaurus"),
        ("Religious", "Religious"),
        ("Science", "Science"),
        ("History", "History"),
        ("Biography / Memoir", "Biography / Memoir"),
        ("Self Help", "Self Help")
    ]
    genre_choices_full = [
        ("Realistic Fiction", "Realistic Fiction"),
        ("Literary Fiction", "Literary Fiction"),
        ("Mystery / Detective Fiction", "Mystery / Detective Fiction"),
        ("Romance", "Romance"),
        ("Historical Fiction", "Historical Fiction"),
        ("Thriller / Horror", "Thriller / Horror"),
        ("Science Fiction", "Science Fiction"),
        ("Fantasy", "Fantasy"),
        ("Children's Books / Early Readers", "Children's Books / Early Readers"),
        ("Young Adult Fiction", "Young Adult Fiction"),
        ("Encyclopedia / General Information", "Encyclopedia / General Information"),
        ("Dictionary / Thesaurus", "Dictionary / Thesaurus"),
        ("Religious", "Religious"),
        ("Science", "Science"),
        ("History", "History"),
        ("Biography / Memoir", "Biography / Memoir"),
        ("Self Help", "Self Help")
    ]
    genre_1 = models.CharField(max_length=35, null=False, choices=genre_choices_abridged)
    genre_2 = models.CharField(max_length=35, null=True, blank=True, choices=genre_choices_full)
    genre_3 = models.CharField(max_length=35, null=True, blank=True, choices=genre_choices_full)
    language = models.CharField(max_length=20,
                                choices=[("English", "English"), ("Spanish / Español", "Spanish / Español")])
    shelf = models.CharField(max_length=10, null=False, default="0", choices=[
        ("1A", "1A"), ("1B", "1B"), ("1C", "1C"),
        ("2A", "2A"), ("2B", "2B"), ("2C", "2C"),
        ("3A", "3A"), ("3B", "3B"), ("3C", "3C"),
        ("4A", "4A"), ("4B", "4B"), ("4C", "4C"),
        ("5A", "5A"), ("5B", "5B"), ("5C", "5C"),
        ("6A", "6A"), ("6B", "6B"), ("6C", "6C"),
        ("7A", "7A"), ("7B", "7B"), ("7C", "7C"),
        ("8A", "8A"), ("8B", "8B"), ("8C", "8C"),
        ("9A", "9A"), ("9B", "9B"), ("9C", "9C"),
        ("10A", "10A"), ("10B", "10B"), ("10C", "10C"),
        ("11A", "11A"), ("11B", "11B"), ("11C", "11C"),
        ("12A", "12A"), ("12B", "12B"), ("12C", "12C"),
        ("13A", "13A"), ("13B", "13B"), ("13C", "13C"),
        ("14A", "14A"), ("14B", "14B"), ("14C", "14C"),
        ("15A", "15A"), ("15B", "15B"), ("15C", "15C"),
        ("16A", "16A"), ("16B", "16B"), ("16C", "16C"),
        ("17A", "17A"), ("17B", "17B"), ("17C", "17C"),
        ("18A", "18A"), ("18B", "18B"), ("18C", "18C"),
        ("0", "0")
    ])
    author2_first = models.CharField(max_length=30, null=True, blank=True)
    author2_middle = models.CharField(max_length=30, null=True, blank=True)
    author2_last = models.CharField(max_length=30, null=True, blank=True)
    author3_first = models.CharField(max_length=30, null=True, blank=True)
    author3_middle = models.CharField(max_length=30, null=True, blank=True)
    author3_last = models.CharField(max_length=30, null=True, blank=True)

    is_series_choices = [(True, "yes"), (False, "no")]
    is_series = models.BooleanField(default=False, null=False, choices=is_series_choices)
    series = models.CharField(max_length=30, null=True, blank=True)

    match_score = 0

    def __str__(self):
        return self.title
