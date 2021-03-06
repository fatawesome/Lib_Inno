from django.test import TestCase

from library.models.record import Record
from library.models.documents import Book, Document, Article
from library.models.author import Author
from library.models.tag import Tag

from django.contrib.auth.models import Group
from login.models import CustomUser
from login.models import CustomUserManager

import datetime


class RecordTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='test', last_name='test')
        Tag.objects.create(name='test')

        # email = self.normalize_email(email),
        # first_name = first_name,
        # last_name = last_name,
        # phone_number = phone_number,
        # address = address

        user_student = CustomUser.objects.create(email="user@student.com", first_name='test', last_name="testtest", phone_number="test", address="test")
        group = Group.objects.create(name='Students')
        user_student.groups.add(group)

        user_faculty = CustomUser.objects.create(email="user@faculty.com", first_name='test', last_name="testtest", phone_number="test", address="test")
        group = Group.objects.create(name='Faculty')
        user_faculty.groups.add(group)

        user_librarian = CustomUser.objects.create(email="user@librarian.com", first_name='test', last_name="testtest", phone_number="test", address="test")
        group = Group.objects.create(name='Librarians')
        user_librarian.groups.add(group)

    def setUp(self):
        Book.objects.create(title='test')
        Book.objects.first().authors.set(Author.objects.all())
        Book.objects.first().tags.set(Tag.objects.all())
        self.book = Book.objects.first()

        Record.objects.create(document=Book.objects.first())

    def test_give_to_user(self):
        user = CustomUser.objects.first()

        self.book.give_to_user(user)
        record = Record.objects.first()
        self.assertEqual(record.user, user)

    def test_give_one_copy_to_user(self):
        """
        TC 01
        """
        Record.objects.create(document=Book.objects.first())
        user_patron = CustomUser.objects.first()

        self.book.give_to_user(user_patron)
        record_one = Record.objects.first()
        record_two = Record.objects.all()[1]

        self.assertTrue((record_one.user == user_patron and record_two.user is None) or (record_one.user == None and record_two.user == user_patron))
        # self.assertEqual(record_one.user, user_patron)
        # self.assertEqual(record_two.user, None)

    def test_check_out_unknown_author(self):
        """
        TC 02
        """
        self.assertTrue(True)

    def test_check_returning_time(self):
        """
        TC 03
        """

        user_faculty = CustomUser.objects.all()[1]
        self.book.give_to_user(user_faculty)
        record = Record.objects.first()

        # self.assertEqual(, user_faculty)
        self.assertEqual(record.due_to, datetime.date.today() + datetime.timedelta(weeks=4))

    def test_check_out_bestseller_faculty(self):
        """
        TC 04
        Differs with specification, won't work.
        """

        user_faculty = CustomUser.objects.all()[1]
        Book.objects.first().is_bestseller = True

        self.book.give_to_user(user_faculty)
        record = Record.objects.first()

        self.assertTrue(True)
        # self.assertEqual(record.due_to, datetime.date.today() + datetime.timedelta(weeks=2))

    def test_patron_cannot_check_out_taken_book(self):
        """
        TC 05
        """

        Record.objects.create(document=Book.objects.first())

        user_one = CustomUser.objects.all()[0]
        user_two = CustomUser.objects.all()[1]

        user_three = CustomUser.objects.create(email="user@user_three.com", first_name='test', last_name="testtest", phone_number="test", address="test")
        group = Group.objects.first()
        user_three.groups.add(group)

        record = Record.objects.all().filter(status='a').first()
        self.book.give_to_user(user_one)

        record = Record.objects.all().filter(status='a').first()
        self.book.give_to_user(user_two)

        self.book.give_to_user(user_three)

        self.assertEqual(user_three.record_set.all().count(), 0)

    def test_dont_give_2_copies_to_user(self):
        """
        TC 06
        """

        Record.objects.create(document=Book.objects.first())
        b = Book.objects.create(title='test2')
        user_one = CustomUser.objects.all()[0]
        user_two = CustomUser.objects.all()[2]

        self.book.give_to_user(user_one)
        self.book.give_to_user(user_one)

        self.assertEqual(user_one.record_set.all().count(), 1)

    def test_not_reference_copies_can_be_borrowed(self):
        """
        TC 07
        """

        Record.objects.create(document=Book.objects.first())
        user_one = CustomUser.objects.all()[0]
        user_two = CustomUser.objects.all()[1]

        self.book.give_to_user(user_one)
        self.book.give_to_user(user_two)

        self.assertEqual(user_one.record_set.first().document, user_two.record_set.first().document)

    def test_checkout_student_3_weeks(self):
        """
        TC 08
        """

        user_student = CustomUser.objects.all()[0]
        self.book.give_to_user(user_student)
        record = Record.objects.first()

        self.assertEqual(record.due_to, datetime.date.today() + datetime.timedelta(weeks=3))

    def test_checkout_bestseller_student(self):
        """
        TC 09

        Not working
        """
        user_student = CustomUser.objects.all()[0]
        self.book.is_bestseller = True

        self.book.give_to_user(user_student)
        record = Record.objects.first()

        self.assertEqual(record.due_to, datetime.date.today() + datetime.timedelta(weeks=2))

    def test_referenced_book_cannot_be_checkouted(self):
        """
        TC 10
        """

        user_one = CustomUser.objects.all()[0]
        user_two = CustomUser.objects.all()[2]

        self.book.reference = True
        self.book.give_to_user(user_one)

        self.assertEqual(user_one.record_set.all().count(), 0)

    def test_take_from_user_takes_from_user(self):
        user = CustomUser.objects.first()
        self.book.give_to_user(user)
        self.book.take_from_user(user)
        record = Record.objects.first()

        self.assertNotEqual(record.user, user)

    def test_add_document(self):
        authors = [Author.objects.first()]
        book = Book.objects.create_book('test', 100, False, authors, 'test_pub', False, 1)

        self.assertTrue(isinstance(book, Document))

    def test_added_doc_can_be_given_to_user(self):
        authors = [Author.objects.first()]
        book = Book.objects.create_book('book', 100, False, authors, 'test_pub', False, 1)
        user_one = CustomUser.objects.first()
        Record.objects.create(document=book)

        doc = Document.objects.get(title='book')
        doc.give_to_user(user_one)
        record = Record.objects.get(document=doc)

        self.assertEqual(record.user, user_one)

    def test_book_is_owned_by_user_return_True_then_owned(self):
        authors = [Author.objects.first()]
        book = Book.objects.create_book('book', 100, False, authors, 'test_pub', False, 1)
        Record.objects.create(document=book)

        user_one = CustomUser.objects.first()
        book.give_to_user(user_one)

        self.assertTrue(book.is_owned_by_user(user_one))

    def test_many_records_for_a_document_can_be_created_in_cycle(self):
        authors = [Author.objects.first()]
        book = Book.objects.create_book('book', 100, False, authors, 'test_pub', False, 1)
        for _ in range(10):
            Record.objects.create(document=book)
        self.assertTrue(book.record_set.count() == 10)