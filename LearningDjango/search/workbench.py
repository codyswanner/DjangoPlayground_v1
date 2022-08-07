if dont_clean_data == "false":
    field_values = [new_book.title, new_book.author_first, new_book.author_middle, new_book.author_last,
                    new_book.author2_first, new_book.author2_middle, new_book.author2_last,
                    new_book.author3_first, new_book.author3_middle, new_book.author3_last,
                    new_book.series]
    for i in field_values:
        if i:
            data_cleaned = titlecase(i)
            i = data_cleaned
        else:
            i = None
