from django.test import TestCase

from library.models.record import Record
from library.models.documents import Book
from library.models.author import Author

from django.contrib.auth.models import User, Group

from login.models import CustomUser
from login.models import CustomUserManager


class TakeFromUserMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='test', last_name='test')
        user = CustomUser.objects.create(email="user@user.com", first_name='test', last_name="testtest",
                                         phone_number="test", address="test")
        groups = Group.objects.create(name='Students')

        user.groups.add(groups)

    def setUp(self):
        book = Book.objects.create(title='test')
        book.authors.set(Author.objects.all())
        self.book = book

        self.record = Record.objects.create(document=self.book)

    def test_take_from_user_takes_from_user(self):
        user = CustomUser.objects.first()
        self.book.give_to_user(user)
        self.book.take_from_user(user)
        record = Record.objects.first()

        self.assertNotEqual(record.user, user)

    def test_take_from_user_reset_status(self):
        user = CustomUser.objects.first()
        self.book.give_to_user(user)
        self.book.take_from_user(user)
        record = Record.objects.first()

        self.assertEqual(record.status, 'a')

    def test_take_from_user_reset_due_to(self):
        user = CustomUser.objects.first()
        self.book.give_to_user(user)
        self.book.take_from_user(user)
        record = Record.objects.first()

        self.assertEqual(record.due_to, None)
