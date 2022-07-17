from django.db import models
import re


# Create your models here.

# The titlecase function *sort of* corrects capitalization mistakes by users.  See notes inside function.
def titlecase(s):
    # This step titlecases the first letter of all words, including trivial words like "and", "the", "of", etc.
    all_titled = re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(),
        s)

    # This step *sort of* lowercases the trivial words.  However, in an effort to avoid inadvertent capturing,
    # the regexp specifies a whitespace on each side of the word.  This causes issues with situations like " And The "
    # because there is only one whitespace in the middle, and therefore only one match, so it will return " and The ",
    # which is incorrect.  Also, worth noting that the all_titled string will have all capitalized words, hence the
    # capitalized words in the capturing group.
    # TODO: make a better regexp for this
    trivials_lowered = re.sub(
        r"\s(The|And|Of|For|In|A|To|An|By|On|That|But|Yet|So|Nor|Or|As|At)\s",
        lambda word: word.group(0).lower(),
        all_titled)

    return trivials_lowered


class Book(models.Model):
    title = models.CharField(max_length=70, null=False)
    author_first = models.CharField(max_length=30, null=False)
    author_middle = models.CharField(max_length=30, null=True, blank=True)
    author_last = models.CharField(max_length=30, null=False)
    genre_1 = models.CharField(max_length=35, null=False, choices=[
        ("Realistic Fiction", "Realistic Fiction"),
        ("Literary Fiction", "Literary Fiction"),
        ("Mystery / Detective Fiction", "Mystery / Detective Fiction"),
        ("Romance", "Romance"),
        ("Historical Fiction", "Historical Fiction"),
        ("Thriller / Horror", "Thriller / Horror"),
        ("Science Fiction", "Science Fiction"),
        ("Fantasy", "Fantasy"),
        ("Children's Books / Early Readers", "Children's Books / Early Readers"),
        ("Biography / Autobiography", "Biography / Autobiography")
    ])
    genre_2 = models.CharField(max_length=35, null=True, blank=True, choices=[
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
        ("Biography / Autobiography", "Biography / Autobiography")
    ])
    genre_3 = models.CharField(max_length=35, null=True, blank=True, choices=[
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
        ("Biography / Autobiography", "Biography / Autobiography")
    ])
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
        ("0", "0")
    ])
    author2_first = models.CharField(max_length=30, blank=True)
    author2_middle = models.CharField(max_length=30, blank=True)
    author2_last = models.CharField(max_length=30, blank=True)
    author3_first = models.CharField(max_length=30, blank=True)
    author3_middle = models.CharField(max_length=30, blank=True)
    author3_last = models.CharField(max_length=30, blank=True)

    is_series_choices = [(True, "yes"), (False, "no")]
    is_series = models.BooleanField(default=False, null=False, choices=is_series_choices)
    series = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.title
