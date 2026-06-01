from app.ai.search_books import get_books_ids, get_book_information, get_books_info_by_query, Book

def test_getting_books_ids_positive():
    response = get_books_ids("Programming")

    assert len(response) == 5
    
def test_getting_books_ids_negative():
    response = get_books_ids("Total fucking boolshit absolute nightmare no books")

    assert not response

def test_getting_book_info_positive():
    book = get_book_information("zyTCAlFPjgYC")

    assert isinstance(book, Book)
    assert book.title == "The Google Story (2018 Updated Edition)"

def test_getting_books_info_positive():
    books = get_books_info_by_query("Programming")

    assert len(books) == 5
    for book in books:
        assert isinstance(book, Book)

def test_getting_books_info_negative():
    books = get_books_info_by_query("Total fucking boolshit absolute nightmare no books")

    assert books == []