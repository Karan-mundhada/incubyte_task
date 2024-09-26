class BookNotFoundError(Exception):
    pass

class BookUnavailableError(Exception):
    pass

class DuplicateBookError(Exception):
    pass

class Book:
    def __init__(self, isbn: str, title: str, author: str, year: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.available = True  # By default, the book is available when added

    def __str__(self):
        availability = "Available" if self.available else "Borrowed"
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {availability}"

class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book: Book):
        if book.isbn in self.books:
            raise DuplicateBookError(f"Book with ISBN {book.isbn} already exists in the library.")
        self.books[book.isbn] = book

    def remove_book(self, isbn: str):
        if isbn not in self.books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")
        book = self.books[isbn]
        if not book.available:
            raise BookUnavailableError(f"Cannot remove '{book.title}' as it is currently borrowed.")
        del self.books[isbn]

    def borrow_book(self, isbn: str):
        if isbn not in self.books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")
        book = self.books[isbn]
        if not book.available:
            raise BookUnavailableError(f"Book '{book.title}' is currently borrowed.")
        book.available = False

    def return_book(self, isbn: str):
        if isbn not in self.books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")
        book = self.books[isbn]
        if book.available:
            raise BookUnavailableError(f"Book '{book.title}' is already available.")
        book.available = True

    def view_available_books(self):
        return [book for book in self.books.values() if book.available]

    def search_books(self, query: str):
        result = [book for book in self.books.values() 
                  if query.lower() in book.title.lower() or query.lower() in book.author.lower()]
        if not result:
            raise BookNotFoundError(f"No books found matching '{query}'.")
        return result
    