# These are custom functions used in this app.


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
