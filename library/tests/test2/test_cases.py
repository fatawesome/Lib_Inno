from django.test import TestCase

from library.models.record import Record
from library.models.documents import *
from library.models.author import Author
from library.models.tag import Tag

from django.contrib.auth.models import Group
from login.models import CustomUser


class TestCases(TestCase):
    @classmethod
    def setUpTestData(cls):

        # creating authors
        # 1st book
        authors_first_book = [
            Author.objects.create(first_name='Thomas H.', last_name='Cormen'),
            Author.objects.create(first_name='Charles E.', last_name='Leiserson'),
            Author.objects.create(first_name='Ronald L.', last_name='Rivest'),
            Author.objects.create(first_name='Clifford', last_name='Stein'),
        ]

        # 2nd book
        authors_second_book = [
            Author.objects.create(first_name='Erich', last_name='Gamma'),
            Author.objects.create(first_name='Ralph', last_name='Johnson'),
            Author.objects.create(first_name='John', last_name='Vlissides'),
            Author.objects.create(first_name='Richard', last_name='Helm'),
        ]

        # 3rd book
        authors_third_book = [
            Author.objects.create(first_name='Brooks', last_name='Jr.'),
            Author.objects.create(first_name='Frederick', last_name='P,'),
        ]

        # file 1
        authors_first_file = [Author.objects.create(first_name='Tony', last_name='Hoare')]

        # file 2
        authors_second_file = [Author.objects.create(first_name='Claude', last_name='Shannon')]

        # creating books
        # book1
        Book.objects.create_book(
            title='Introduction to Algorithms',
            publisher='MIT Press',
            edition=3,
            year=2009,
            is_bestseller=False,
            authors=authors_first_book,
            price=10,
        )

        #book2
        Book.objects.create_book(
            title='Design Patterns: Elements of Reusable Object-Oriented Software',
            publisher='Addison-Wesley Professional',
            edition=1,
            year=2003,
            is_bestseller=True,
            authors=authors_second_book,
            price=10,
        )

        # book3
        Book.objects.create_book(
            title='The Mythical Man-month',
            publisher='Addison-Wesley Longman Publishing Co., Inc.',
            edition=2,
            year=1995,
            is_bestseller=True,
            authors=authors_second_book,
            reference=True,
            price=10,
        )

        # creating files
        # file 1
        Audio.objects.create_audio(
            title='Null References: The Billion Dollar Mistake',
            authors=authors_first_file,
            price=10,
            content='Blank',
        )

        # file 2
        Video.objects.create_video(
            title=' Information Entropy',
            authors=authors_second_file,
            price=10,
            content='Blank',
        )

        

