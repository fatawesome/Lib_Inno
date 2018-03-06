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
        b1 = Book.objects.create_book(
            title='Introduction to Algorithms',
            publisher='MIT Press',
            edition=3,
            year=2009,
            is_bestseller=False,
            authors=authors_first_book,
            price=10,
            reference=False,
        )

        # book2
        b2 = Book.objects.create_book(
            title='Design Patterns: Elements of Reusable Object-Oriented Software',
            publisher='Addison-Wesley Professional',
            edition=1,
            year=2003,
            is_bestseller=True,
            authors=authors_second_book,
            price=10,
            reference=False,
        )

        # book3
        b3 = Book.objects.create_book(
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
        av1 = Audio.objects.create_audio(
            title='Null References: The Billion Dollar Mistake',
            authors=authors_first_file,
            price=10,
            content='Blank',
        )

        # file 2
        av2 = Video.objects.create_video(
            title='Information Entropy',
            authors=authors_second_file,
            price=10,
            content='Blank',
        )

        for _ in range(3):
            Record.objects.create(document=b1)

        for _ in range(2):
            Record.objects.create(document=b2)

        Record.objects.create(document=b3)

        Record.objects.create(document=av1)
        Record.objects.create(document=av2)

        # group Faculty
        group_faculty = Group.objects.create(name='Faculty')
        group_students = Group.objects.create(name="Students")
        group_librarian = Group.objects.create(name="Librarian")

        # first user
        CustomUser.objects.create_user(
            email="p1@mail.ru", first_name="Sergey", last_name="Afonso", address="Via Margutta, 3", phone_number='30001'
        )

        CustomUser.objects.filter(first_name="Sergey", last_name="Afonso").first().groups.add(group_faculty)

        # second user
        p2 = CustomUser.objects.create_user(
            email="p2@mail.ru", first_name="Nadia", last_name="Teixerina", address="Via Scara, 13", phone_number='30002'
        )

        p2.groups.add(group_students)

        # third user
        CustomUser.objects.create_user(
            email="p3@mail.ru", first_name="Elvira", last_name="Espindola", address="Via del Corso, 22", phone_number='30003'
        )

        CustomUser.objects.filter(first_name="Elvira", last_name="Espindola").first().groups.add(group_students)

        #4th user
        lib = CustomUser.objects.create_user(
            email="lib@mail.ru", first_name="Librarian_first_name", last_name="Librarian_last_name", address="Via del Corso, 22", phone_number='30003'
        )

        lib.groups.add(group_librarian)

    def test_librarian_add_documents_and_users(self):
        """
        TC 1
        """
        self.assertTrue(Document.objects.count() == 5 and CustomUser.objects.count() == 4)

    def test_librarian_can_add_record(self):
        """
        TC 1
        """

        self.assertEqual(Record.objects.count(), 8)

    def test_librarian_can_remove_books_and_patrons(self):
        """
        TC 2
        """
        b1 = Document.objects.filter(title='Introduction to Algorithms').first()
        b3 = Document.objects.filter(title='The Mythical Man-month').first()
        p2 = CustomUser.objects.get(pk=2)

        b1.record_set.first().delete()
        b1.record_set.first().delete()
        b3.record_set.first().delete()

        p2.delete_user()

        self.assertTrue(Record.objects.count() == 5 and CustomUser.objects.count() == 3)

    def test_librarian_check_users(self):
        """
        TC 3
        """

        """Initial state"""
        b1 = Document.objects.filter(title='Introduction to Algorithms').first()
        b3 = Document.objects.filter(title='The Mythical Man-month').first()
        p2 = CustomUser.objects.get(pk=2)

        b1.record_set.first().delete()
        b1.record_set.first().delete()
        b3.record_set.first().delete()

        p2.delete_user()
        """Initial state"""

        p1 = CustomUser.objects.get(pk=1)
        self.assertTrue(p1.first_name=="Sergey" and p1.last_name=="Afonso" and p1.address=="Via Margutta, 3" and p1.phone_number=='30001')
        self.assertTrue('Faculty' in [x.name for x in p1.groups.all()] and p1.groups.count() == 1)
        self.assertTrue(p1.record_set.count() == 0)

        p3 = CustomUser.objects.get(pk=3)
        self.assertTrue(p3.first_name=="Elvira" and p3.last_name=="Espindola" and p3.address=="Via del Corso, 22" and p3.phone_number=='30003')
        self.assertTrue('Students' in [x.name for x in p3.groups.all()] and p3.groups.count() == 1)
        self.assertTrue(p3.record_set.count() == 0)

    def test_librarian_try_to_check_not_existing_user(self):
        """
        TC 4
        """

        """Initial state"""
        b1 = Document.objects.filter(title='Introduction to Algorithms').first()
        b3 = Document.objects.filter(title='The Mythical Man-month').first()
        p2 = CustomUser.objects.get(pk=2)

        b1.record_set.first().delete()
        b1.record_set.first().delete()
        b3.record_set.first().delete()

        p2.delete_user()
        """Initial state"""

        self.assertTrue(CustomUser.objects.filter(id=2).count() == 0)

        p3 = CustomUser.objects.get(pk=3)
        self.assertTrue(
            p3.first_name == "Elvira" and p3.last_name == "Espindola" and p3.address == "Via del Corso, 22" and p3.phone_number == '30003')
        self.assertTrue('Students' in [x.name for x in p3.groups.all()] and p3.groups.count() == 1)
        self.assertTrue(p3.record_set.count() == 0)

    def test_patron_check_out_book(self):
        """
        TC 5
        """
        """Initial state"""
        b1 = Document.objects.filter(title='Introduction to Algorithms').first()
        b3 = Document.objects.filter(title='The Mythical Man-month').first()
        p2 = CustomUser.objects.get(id=2)

        b1.record_set.first().delete()
        b1.record_set.first().delete()
        b3.record_set.first().delete()

        p2.delete_user()
        """Initial state"""

        self.assertTrue(CustomUser.objects.filter(id=2).count() == 0)

        # b1.give_to_user(p2)

