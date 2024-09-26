# test_library_management.py
import unittest
from main import Book, Library, DuplicateBookError, BookNotFoundError, BookUnavailableError

class TestLibraryManagement(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.book1 = Book(isbn="1234", title="Clean Code", author="Robert C. Martin", year=2008)
        self.book2 = Book(isbn="5678", title="The Pragmatic Programmer", author="Andrew Hunt", year=1999)
        self.book3 = Book(isbn="9101", title="Code Complete", author="Steve McConnell", year=2004)
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)

    def test_add_book(self):
        new_book = Book(isbn="9999", title="Refactoring", author="Martin Fowler", year=1999)
        self.library.add_book(new_book)
        self.assertIn("9999", self.library.books)

    def test_add_duplicate_book(self):
        with self.assertRaises(DuplicateBookError):
            self.library.add_book(self.book1)  # Duplicate ISBN

    def test_borrow_book_success(self):
        self.library.borrow_book("1234")
        self.assertFalse(self.book1.available)

    def test_borrow_book_unavailable(self):
        self.library.borrow_book("1234")
        with self.assertRaises(BookUnavailableError):
            self.library.borrow_book("1234")  # Already borrowed

    def test_borrow_nonexistent_book(self):
        with self.assertRaises(BookNotFoundError):
            self.library.borrow_book("9999")  # ISBN not in library

    def test_return_book_success(self):
        self.library.borrow_book("1234")
        self.library.return_book("1234")
        self.assertTrue(self.book1.available)

    def test_return_book_already_available(self):
        with self.assertRaises(BookUnavailableError):
            self.library.return_book("1234")  # Already available

    def test_view_available_books(self):
        self.library.borrow_book("1234")
        available_books = self.library.view_available_books()
        self.assertIn(self.book2, available_books)
        self.assertNotIn(self.book1, available_books)

    def test_remove_book_success(self):
        self.library.remove_book("1234")
        self.assertNotIn("1234", self.library.books)

    def test_remove_nonexistent_book(self):
        with self.assertRaises(BookNotFoundError):
            self.library.remove_book("9999")  # ISBN not in library

    def test_remove_borrowed_book(self):
        self.library.borrow_book("1234")
        with self.assertRaises(BookUnavailableError):
            self.library.remove_book("1234")  # Cannot remove borrowed book

    def test_search_books_by_title(self):
        results = self.library.search_books("Clean Code")
        self.assertIn(self.book1, results)
        self.assertNotIn(self.book2, results)

    def test_search_books_by_author(self):
        results = self.library.search_books("Steve McConnell")
        self.assertIn(self.book3, results)
        self.assertNotIn(self.book2, results)

    def test_search_books_no_match(self):
        with self.assertRaises(BookNotFoundError):
            self.library.search_books("Nonexistent Book")

    def test_custom_exceptions(self):
        with self.assertRaises(DuplicateBookError):
            self.library.add_book(self.book1)  # Adding duplicate ISBN
        with self.assertRaises(BookNotFoundError):
            self.library.borrow_book("9999")  # Non-existent book

if __name__ == '__main__':
    unittest.main()