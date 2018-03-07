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

    def setup_remove(self):
        b1 = Document.objects.filter(title='Introduction to Algorithms').first()
        b3 = Document.objects.filter(title='The Mythical Man-month').first()
        p2 = CustomUser.objects.get(pk=2)

        b1.record_set.first().delete()
        b1.record_set.first().delete()
        b3.record_set.first().delete()

        p2.delete_user()

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
        self.setup_remove()

        self.assertTrue(Record.objects.count() == 5 and CustomUser.objects.count() == 3)

    def test_librarian_check_users(self):
        """
        TC 3
        """
        self.setup_remove()

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
        self.setup_remove()

        self.assertTrue(CustomUser.objects.filter(id=2).count() == 0)

        p3 = CustomUser.objects.get(pk=3)
        self.assertTrue(p3.first_name == "Elvira" and p3.last_name == "Espindola" and p3.address == "Via del Corso, 22" and p3.phone_number == '30003')
        self.assertTrue('Students' in [x.name for x in p3.groups.all()] and p3.groups.count() == 1)
        self.assertTrue(p3.record_set.count() == 0)

    def test_not_existing_patron_check_out_book(self):
        """
        TC 5
        """
        self.setup_remove()

        self.assertTrue(CustomUser.objects.filter(id=2).count() == 0)

        #b1.give_to_user(p2)

    def test_patrons_check_out_books(self):
        """
        TC 6      INCORRECT TEST CASE
        """
        self.setup_remove()

        p1 = CustomUser.objects.get(id=1)
        p3 = CustomUser.objects.get(id=3)

        b1 = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first())


        self.assertTrue(p3.record_set.filter(document=b1).count() == 0)
        #b1.reserve_by_user(p3)
        #b1.give_to_user(p3, p3.record_set.filter(document=b1).first())

        b2.reserve_by_user(p1)
        b2.give_to_user(p1, p1.record_set.filter(document=b2).first())

        self.assertTrue(p1.first_name == "Sergey" and p1.last_name == "Afonso" and p1.address == "Via Margutta, 3" and p1.phone_number == '30001')
        self.assertTrue('Faculty' in [x.name for x in p1.groups.all()] and p1.groups.count() == 1)
        self.assertTrue(p1.record_set.count() == 2 and p1.record_set.filter(document=b1).count() == 1 and p1.record_set.filter(document=b2).count() == 1)
        self.assertTrue(p1.record_set.filter(document=b1).first().due_to == datetime.date.today() + datetime.timedelta(weeks=4))

        self.assertTrue(p3.first_name == "Elvira" and p3.last_name == "Espindola" and p3.address == "Via del Corso, 22" and p3.phone_number == '30003')
        self.assertTrue('Students' in [x.name for x in p3.groups.all()] and p3.groups.count() == 1)
        self.assertTrue(p3.record_set.count() == 0)

    def test_patrons_check_out_existing_and_not_documents(self):
        """
        TC 7
        """

        p1 = CustomUser.objects.get(id=1)
        p2 = CustomUser.objects.get(id=2)

        b1 = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)
        b3 = Book.objects.get(id=3)

        av1 = Audio.objects.get(id=4)
        av2 = Video.objects.get(id=5)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first())

        b2.reserve_by_user(p1)
        b2.give_to_user(p1, p1.record_set.filter(document=b2).first())

        b3.reserve_by_user(p1)
        self.assertTrue(p1.record_set.filter(document=b3).count() == 0) # user can not take a reference book
        #b3.give_to_user(p1, p1.record_set.filter(document=b3).first())

        av1.reserve_by_user(p1)
        av1.give_to_user(p1, p1.record_set.filter(document=av1).first())

        b1.reserve_by_user(p2)
        b1.give_to_user(p2, p2.record_set.filter(document=b1).first())

        b2.reserve_by_user(p2)
        b2.give_to_user(p2, p2.record_set.filter(document=b2).first())

        av2.reserve_by_user(p2)
        av2.give_to_user(p2, p2.record_set.filter(document=av2).first())

        self.assertTrue(p1.first_name == "Sergey" and p1.last_name == "Afonso" and p1.address == "Via Margutta, 3" and p1.phone_number == '30001')
        self.assertTrue('Faculty' in [x.name for x in p1.groups.all()] and p1.groups.count() == 1)
        self.assertTrue(p1.record_set.count() == 3 and p1.record_set.filter(document=b1).count() == 1 and p1.record_set.filter(document=b2).count() == 1 and p1.record_set.filter(document=av1).count() == 1)
        self.assertTrue(p1.record_set.filter(document=b1).first().due_to == datetime.date.today() + datetime.timedelta(weeks=4))
        self.assertTrue(p1.record_set.filter(document=b2).first().due_to == datetime.date.today() + datetime.timedelta(weeks=4))
        self.assertTrue(p1.record_set.filter(document=av1).first().due_to == datetime.date.today() + datetime.timedelta(weeks=2))

        self.assertTrue(p2.first_name=="Nadia" and p2.last_name=="Teixerina" and p2.address=="Via Scara, 13" and p2.phone_number=='30002')
        self.assertTrue('Students' in [x.name for x in p2.groups.all()] and p2.groups.count() == 1)
        self.assertTrue(p2.record_set.count() == 3 and p2.record_set.filter(document=b1).count() == 1 and p2.record_set.filter(document=b2).count() == 1 and p2.record_set.filter(document=av2).count() == 1)
        self.assertTrue(p2.record_set.filter(document=b1).first().due_to == datetime.date.today() + datetime.timedelta(weeks=3))
        self.assertTrue(p2.record_set.filter(document=b2).first().due_to == datetime.date.today() + datetime.timedelta(weeks=2))
        self.assertTrue(p2.record_set.filter(document=av2).first().due_to == datetime.date.today() + datetime.timedelta(weeks=2))

    def test_check_overdue(self):
        """
        TC 8
        """
        p1 = CustomUser.objects.get(id=1)
        p2 = CustomUser.objects.get(id=2)

        b1 = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)
        av1 = Audio.objects.get(id=4)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first(), date=datetime.date(year=2018, month=2, day=9))
        b2.reserve_by_user(p1)
        b2.give_to_user(p1, p1.record_set.filter(document=b2).first(), date=datetime.date(year=2018, month=2, day=2))

        b1.reserve_by_user(p2)
        b1.give_to_user(p2, p2.record_set.filter(document=b1).first(), date=datetime.date(year=2018, month=2, day=5))
        av1.reserve_by_user(p2)
        av1.give_to_user(p1, p2.record_set.filter(document=av1).first(), date=datetime.date(year=2018, month=2, day=17))

        self.assertEqual(p1.record_set.filter(document=b2).first().get_overdue(), 3 + 2)
        self.assertEqual(p2.record_set.filter(document=b1).first().get_overdue(), 7 + 2)
        self.assertEqual(p2.record_set.filter(document=av1).first().get_overdue(), 2 + 2)
