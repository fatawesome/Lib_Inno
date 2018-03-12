from django.test import TestCase
from django.contrib.auth.models import Group

from login.models import *
from library.models import *

import datetime


class TestCases(TestCase):
    def setUp(self):
        self.author = Author.objects.create_author(
            first_name='test',
            last_name='test',
            date_of_birth=datetime.date(year=1990, month=1, day=1),
            date_of_death=datetime.date(year=1991, month=1, day=1)
        )

        list_of_authors = [self.author]
        self.book = Book.objects.create_book(
            title='test',
            price=10,
            reference=False,
            authors=list_of_authors,
            publisher='test',
            is_bestseller=False,
            year=1990,
            edition=1,
        )
        self.book_copy = Record.objects.create(document=self.book)

        self.group_faculty = Group.objects.create(name='Faculty')
        self.group_students = Group.objects.create(name="Students")

        self.faculty_user = CustomUser.objects.create_user(
            email='test1@test.com',
            first_name='test',
            last_name='test',
            phone_number=12345,
            address='test',
            password=123,
        )
        self.faculty_user.groups.add(self.group_faculty)

        self.student_user = CustomUser.objects.create_user(
            email='student@test.com',
            first_name='student',
            last_name='student',
            phone_number=123,
            address='test',
            password=1234,
        )
        self.student_user.groups.add(self.group_students)

    def test_get_overdue_fine_for_1_day(self):
        student = CustomUser.objects.all()[1]
        book = Book.objects.first()
        book.reserve_by_user(user=student)
        record = Record.objects.first()
        book.give_to_user(user=student, record=record,
                          date=datetime.date(year=2018, month=2, day=12))

        self.assertEqual(record.get_overdue_fine(), 200 + 200)
