from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()
GOOGLE_API_TOKEN = getenv("GOOGLE_DATA_API_KEY")

class Book:
    def __init__(self, url: str, title: str, description: str, authors: list[str], pages_count: int, published_date: str):
        self.url = url
        self.title = title
        self.description = description
        self.authors = authors
        self.pages_count = pages_count
        self.published_date = published_date

def get_books_ids(query: str) -> list[str]:
    url = f"https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "key": GOOGLE_API_TOKEN,
        "maxResults": 5
    }
    
    response = requests.get(url, params)
    data = response.json()

    if "items" not in data.keys():
        return []

    books_ids = []
    for book in data["items"]:
        book_id = book["id"]
        if book_id:
            books_ids.append(book_id)

    return books_ids

def get_book_information(id: str) -> Book:
    url = f"https://www.googleapis.com/books/v1/volumes/{id}"
    params = {
        "key": GOOGLE_API_TOKEN
    }
    response = requests.get(url, params)


    data = response.json()
    book_url = data["volumeInfo"]["infoLink"]
    title = data["volumeInfo"]["title"]
    description = data["volumeInfo"].get("description", "No description.")
    authors = data["volumeInfo"].get("authors", "No authors signed.")
    pages_count = data["volumeInfo"].get("pageCount", 0)
    published_date = data["volumeInfo"].get("publishedDate", "No published date.")

    return Book(book_url, title, description, authors, pages_count, published_date)

def get_books_info_by_query(query: str) -> list[Book]:
    books_ids = get_books_ids(query)

    if not books_ids:
        return []
    
    books = []
    
    for book_id in books_ids:
        books.append(get_book_information(book_id))

    return books