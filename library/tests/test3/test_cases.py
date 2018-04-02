from django.test import TestCase

from library.models.record import Record
from library.models.documents import *
from library.models.author import Author

from django.contrib.auth.models import Group
from login.models import CustomUser

from datetime import timedelta


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

        # file 1
        authors_first_file = [Author.objects.create(first_name='Tony', last_name='Hoare')]

        # creating books
        # book1
        b1 = Book.objects.create_book(
            title='Introduction to Algorithms',
            publisher='MIT Press',
            edition=3,
            year=2009,
            is_bestseller=False,
            authors=authors_first_book,
            price=5000,
            reference=False,
        )

        for _ in range(3):
            Record.objects.create(document=b1)

        # book2
        b2 = Book.objects.create_book(
            title='Design Patterns: Elements of Reusable Object-Oriented Software',
            publisher='Addison-Wesley Professional',
            edition=1,
            year=2003,
            is_bestseller=True,
            authors=authors_second_book,
            price=1700,
            reference=False,
        )

        for _ in range(3):
            Record.objects.create(document=b2)

        # creating files
        # file 1
        av1 = Audio.objects.create_audio(
            title='Null References: The Billion Dollar Mistake',
            authors=authors_first_file,
            price=700,
            content='Blank',
        )

        for _ in range(2):
            Record.objects.create(document=av1)

        # group Faculty
        group_faculty = Group.objects.create(name='Faculty')
        group_students = Group.objects.create(name="Students")
        group_visiting_profs = Group.objects.create(name="Visiting Professors")

        # first user
        afonso = CustomUser.objects.create_user(
            email="p1@mail.ru", first_name="Sergey", last_name="Afonso", address="Via Margutta, 3", phone_number='30001'
        )
        afonso.groups.add(group_faculty)
        afonso.subtype = 'Professors'

        # second user
        nadia = CustomUser.objects.create_user(
            email="p2@mail.ru", first_name="Nadia", last_name="Teixerina", address="Via Scara, 13", phone_number='30002'
        )
        nadia.groups.add(group_faculty)
        nadia.subtype = 'Professors'

        # third user
        elvira = CustomUser.objects.create_user(
            email="p3@mail.ru", first_name="Elvira", last_name="Espindola", address="Via del Corso, 22",
            phone_number='30003'
        )
        elvira.groups.add(group_faculty)
        elvira.subtype = 'Professors'

        # 4th user
        elvira = CustomUser.objects.create_user(
            email="p4@mail.ru", first_name="Andrey", last_name="Velo", address="Avenida Mazatlan 250",
            phone_number='30004'
        )
        elvira.groups.add(group_students)
        elvira.subtype = 'Students'

        # 5th user
        elvira = CustomUser.objects.create_user(
            email="p5@mail.ru", first_name="Veronika", last_name="Rama", address="Stret Atocha, 27",
            phone_number='30005'
        )
        elvira.groups.add(group_visiting_profs)
        elvira.subtype = 'Visiting Professors'

        # liiiiibrarian
        lib = CustomUser.objects.create_user(
            email="lib@mail.ru", first_name="Librarian_first_name", last_name="Librarian_last_name",
            address="Innopolis, 1", phone_number='3000234'
        )

    def test_no_overdue(self):
        """
        TC 01
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        b1 = Book.objects.first()
        b2 = Book.objects.get(id=2)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first(), date=datetime.date(year=2018, month=3, day=5))
        b2.reserve_by_user(p1)
        b2.give_to_user(p1, p1.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=5))

        record_two = p1.record_set.get(document=b2)
        self.assertEqual(record_two.get_overdue_fine(), 0)

        b2.take_from_user(p1)
        record_one = p1.record_set.get(document=b1)
        self.assertEqual(record_one.get_overdue(), 0)
