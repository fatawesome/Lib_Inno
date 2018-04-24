from django.test import TestCase
from library.models.request_queue import RequestQueueElement
from library.models.record import Record
from library.models.documents import *
from library.models.author import Author
from django.test.client import RequestFactory
from django.contrib.auth.models import Group
from login.models import CustomUser

from datetime import timedelta

end_march = 30


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
        cls.av1 = Audio.objects.create_audio(
            title='Null References: The Billion Dollar Mistake',
            authors=authors_first_file,
            price=700,
            content='Blank',
        )

        for _ in range(2):
            Record.objects.create(document=cls.av1)

        # group Faculty
        group_faculty = Group.objects.create(name='Faculty')
        group_students = Group.objects.create(name="Students")
        group_visiting_profs = Group.objects.create(name="Visiting Professors")

        # first user
        afonso = CustomUser.objects.create_user(
            email="p1@mail.ru", first_name="Sergey", last_name="Afonso", address="Via Margutta, 3",
            phone_number='30001', password='temporary'
        )
        afonso.groups.add(group_faculty)
        afonso.subtype = 'Professors'
        afonso.save()

        # second user
        nadia = CustomUser.objects.create_user(
            email="p2@mail.ru", first_name="Nadia", last_name="Teixerina", address="Via Scara, 13",
            phone_number='30002', password='temporary'
        )
        nadia.groups.add(group_faculty)
        nadia.subtype = 'Professors'
        nadia.save()

        # third user
        elvira = CustomUser.objects.create_user(
            email="p3@mail.ru", first_name="Elvira", last_name="Espindola", address="Via del Corso, 22",
            password='temporary',
            phone_number='30003'
        )
        elvira.groups.add(group_faculty)
        elvira.subtype = 'Professors'
        elvira.save()

        # 4th user
        elvira = CustomUser.objects.create_user(
            email="p4@mail.ru", first_name="Andrey", last_name="Velo", address="Avenida Mazatlan 250",
            password='temporary',
            phone_number='30004'
        )
        elvira.groups.add(group_students)
        elvira.subtype = 'Students'
        elvira.save()  # ПОЧЕМУ АНДРЕЯ ЗОВУТ ЭЛЬВИРА БЛЯДЬ

        # 5th user
        elvira = CustomUser.objects.create_user(
            email="p5@mail.ru", first_name="Veronika", last_name="Rama", address="Stret Atocha, 27",
            password='temporary',
            phone_number='30005'
        )
        elvira.groups.add(group_visiting_profs)
        elvira.subtype = 'Visiting Professors'
        elvira.save()

        # liiiiibrarian
        lib = CustomUser.objects.create_user(
            email="lib@mail.ru", first_name="Librarian_first_name", last_name="Librarian_last_name",
            address="Innopolis, 1", phone_number='3000234'
        )

    def test_one(self):
        """
        TC 01
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        b1 = Book.objects.first()
        b2 = Book.objects.get(id=2)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first(), datetime.date(year=2018, month=3, day=5))
        b2.reserve_by_user(p1)
        b2.give_to_user(p1, p1.record_set.get(document=b2), datetime.date(year=2018, month=3, day=5))

        record_two = p1.record_set.get(document=b2)
        self.assertEqual(record_two.get_overdue_fine(datetime.date(year=2018, month=4, day=2)), 0)

        b2.take_from_user(p1)
        record_one = p1.record_set.get(document=b1)
        self.assertEqual(record_one.get_overdue(datetime.date(year=2018, month=4, day=2)), 0)

    def test_two(self):
        """
        TC 02
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')

        b1 = Book.objects.first()
        b2 = Book.objects.get(id=2)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first(), date=datetime.date(year=2018, month=3, day=5))
        b2.reserve_by_user(p1)
        b2.give_to_user(p1, p1.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=5))

        b1.reserve_by_user(s)
        b1.give_to_user(s, s.record_set.filter(document=b1).first(), date=datetime.date(year=2018, month=3, day=5))
        b2.reserve_by_user(s)
        b2.give_to_user(s, s.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=5))

        b1.reserve_by_user(v)
        b1.give_to_user(v, v.record_set.filter(document=b1).first(), date=datetime.date(year=2018, month=3, day=5))
        b2.reserve_by_user(v)
        b2.give_to_user(v, v.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=5))

        self.assertEqual(p1.record_set.get(document=b1).get_overdue(datetime.date(year=2018, month=4, day=2)), 0)
        self.assertEqual(p1.record_set.get(document=b1).get_overdue_fine(datetime.date(year=2018, month=4, day=2)), 0)
        self.assertEqual(p1.record_set.get(document=b2).get_overdue(datetime.date(year=2018, month=4, day=2)), 0)
        self.assertEqual(p1.record_set.get(document=b2).get_overdue_fine(datetime.date(year=2018, month=4, day=2)), 0)

        self.assertEqual(s.record_set.get(document=b1).get_overdue(datetime.date(year=2018, month=4, day=2)), 7)
        self.assertEqual(s.record_set.get(document=b1).get_overdue_fine(datetime.date(year=2018, month=4, day=2)), 700)
        self.assertEqual(s.record_set.get(document=b2).get_overdue(datetime.date(year=2018, month=4, day=2)), 14)
        self.assertEqual(s.record_set.get(document=b2).get_overdue_fine(datetime.date(year=2018, month=4, day=2)), 1400)

        self.assertEqual(v.record_set.get(document=b1).get_overdue(datetime.date(year=2018, month=4, day=2)), 21)
        self.assertEqual(v.record_set.get(document=b1).get_overdue_fine(datetime.date(year=2018, month=4, day=2)), 2100)
        self.assertEqual(v.record_set.get(document=b2).get_overdue(datetime.date(year=2018, month=4, day=2)), 21)
        self.assertEqual(v.record_set.get(document=b2).get_overdue_fine(datetime.date(year=2018, month=4, day=2)), 1700)

    def test_three(self):
        """
        TC 03
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')

        b1 = Book.objects.first()
        b2 = Book.objects.get(id=2)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first(), date=datetime.date(year=2018, month=3, day=29))
        p1_record_of_d1 = p1.record_set.get(document=b1)
        p1_record_of_d1.renew_by_user(p1, date=datetime.date(year=2018, month=4, day=2))

        b2.reserve_by_user(s)
        b2.give_to_user(s, s.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=29))
        s_record_of_d2 = s.record_set.get(document=b2)
        s_record_of_d2.renew_by_user(s, date=datetime.date(year=2018, month=4, day=2))

        b2.reserve_by_user(v)
        b2.give_to_user(v, v.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=29))
        v_record_of_d2 = v.record_set.get(document=b2)
        v_record_of_d2.renew_by_user(v, date=datetime.date(year=2018, month=4, day=2))

        self.assertEqual(p1_record_of_d1.due_to, datetime.date(year=2018, month=4, day=30))
        self.assertEqual(s_record_of_d2.due_to, datetime.date(year=2018, month=4, day=16))
        self.assertEqual(v_record_of_d2.due_to, datetime.date(year=2018, month=4, day=9))

    def test_four(self):
        """
        TC 04
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')

        b1 = Book.objects.first()
        b2 = Book.objects.get(id=2)

        b1.reserve_by_user(p1)
        b1.give_to_user(p1, p1.record_set.filter(document=b1).first(),
                        date=datetime.date(year=2018, month=3, day=29))
        p1_record_of_d1 = p1.record_set.get(document=b1)
        p1_record_of_d1.renew_by_user(p1, date=datetime.date(year=2018, month=4, day=2))

        b2.reserve_by_user(s)
        b2.give_to_user(s, s.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=29))
        s_record_of_d2 = s.record_set.get(document=b2)

        b2.reserve_by_user(v)
        b2.give_to_user(v, v.record_set.get(document=b2), date=datetime.date(year=2018, month=3, day=29))
        v_record_of_d2 = v.record_set.get(document=b2)

        b2.outstanding = True
        b2.save()
        s_record_of_d2.renew_by_user(s, date=datetime.date(year=2018, month=4, day=2))
        v_record_of_d2.renew_by_user(v, date=datetime.date(year=2018, month=4, day=2))

        self.assertEqual(p1_record_of_d1.due_to, datetime.date(year=2018, month=4, day=30))
        self.assertEqual(v_record_of_d2.due_to, datetime.date(year=2018, month=4, day=5))
        self.assertEqual(s_record_of_d2.due_to, datetime.date(year=2018, month=4, day=12))

    def login_and_check_out(self, part_of_mail, user: CustomUser, document, year=2018, month=3, day=29):
        """
        Imitates login in the system, takes function of templates
        :param part_of_mail: fill a gap in the user's email in format p{part_of_mail}@mail.ru
        :param user: object type CustomUser
        :param document:object type Document
        :param year:
        :param month:
        :param day:
        """

        self.client.login(username='p{}@mail.ru'.format(part_of_mail), password='temporary')
        if document.record_set.filter(status='a').count() == 0:
            response = self.client.get('/document/{}/get_in_queue/'.format(document.id), follow=True)
        else:
            document.reserve_by_user(user)
            document.give_to_user(user, user.record_set.get(document=document),
                                  date=datetime.date(year=year, month=month, day=day))

    def test_five(self):
        """
        TC 05
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')
        av1 = Audio.objects.first()
        self.login_and_check_out(part_of_mail=1, user=p1, document=av1)
        self.login_and_check_out(part_of_mail=4, user=s, document=av1)
        self.login_and_check_out(part_of_mail=5, user=v, document=av1)
        self.assertEqual(str(self.av1.requestqueueelement_set.all()), "<QuerySet [<RequestQueueElement: p5@mail.ru>]>")

    def test_six(self):
        """
        TC 06
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')
        p2 = CustomUser.objects.get(first_name='Elvira')
        p3 = CustomUser.objects.get(first_name='Nadia')
        av1 = Audio.objects.first()
        self.login_and_check_out(part_of_mail=1, user=p1, document=av1)
        self.login_and_check_out(part_of_mail=2, user=p2, document=av1)
        self.login_and_check_out(part_of_mail=4, user=s, document=av1)
        self.login_and_check_out(part_of_mail=5, user=v, document=av1)
        self.login_and_check_out(part_of_mail=3, user=p3, document=av1)
        self.assertEqual(
            str(self.av1.requestqueueelement_set.all()),
            "<QuerySet [<RequestQueueElement: p4@mail.ru>, <RequestQueueElement: p5@mail.ru>, <RequestQueueElement: p3@mail.ru>]>")

    def test_seven(self):
        """
        TC 07
        """
        # A part from the sixth test
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')
        p2 = CustomUser.objects.get(first_name='Elvira')
        p3 = CustomUser.objects.get(first_name='Nadia')
        av1 = Audio.objects.first()
        self.login_and_check_out(part_of_mail=1, user=p1, document=av1)
        self.login_and_check_out(part_of_mail=2, user=p2, document=av1)
        self.login_and_check_out(part_of_mail=4, user=s, document=av1)
        self.login_and_check_out(part_of_mail=5, user=v, document=av1)
        self.login_and_check_out(part_of_mail=3, user=p3, document=av1)

        # Test 7
        self.av1.outstanding_request()
        self.assertEqual(
            "<QuerySet []>",
            str(self.av1.requestqueueelement_set.all())
        )

    def test_eight(self):
        """
        TC 08
        """
        # A part from the sixth test
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')
        p2 = CustomUser.objects.get(first_name='Elvira')
        p3 = CustomUser.objects.get(first_name='Nadia')
        av1 = Audio.objects.first()
        self.login_and_check_out(part_of_mail=1, user=p1, document=av1)
        self.login_and_check_out(part_of_mail=2, user=p2, document=av1)
        self.login_and_check_out(part_of_mail=4, user=s, document=av1)
        self.login_and_check_out(part_of_mail=5, user=v, document=av1)
        self.login_and_check_out(part_of_mail=3, user=p3, document=av1)

        # Test 8
        av1.take_from_user(p2)
        self.assertEqual('<QuerySet []>', str(p2.record_set.filter(document=av1)))

    def test_nine(self):
        """
        TC 09
        """
        # A part from the sixth test
        p1 = CustomUser.objects.get(last_name='Afonso')
        s = CustomUser.objects.get(last_name='Velo')
        v = CustomUser.objects.get(last_name='Rama')
        p2 = CustomUser.objects.get(first_name='Elvira')
        p3 = CustomUser.objects.get(first_name='Nadia')
        av1 = Audio.objects.first()
        self.login_and_check_out(part_of_mail=1, user=p1, document=av1)
        self.login_and_check_out(part_of_mail=2, user=p2, document=av1)
        self.login_and_check_out(part_of_mail=4, user=s, document=av1)
        self.login_and_check_out(part_of_mail=5, user=v, document=av1)
        self.login_and_check_out(part_of_mail=3, user=p3, document=av1)

        # Test 9
        p1.record_set.get(document=av1).renew_by_user(p1, date=datetime.date(year=2018, month=3, day=2))
        self.assertEqual(p1.record_set.filter(document=av1).first().document.title, "Null References: The Billion Dollar Mistake")
        self.assertEqual(
            '<QuerySet [<RequestQueueElement: p4@mail.ru>, <RequestQueueElement: p5@mail.ru>, <RequestQueueElement: p3@mail.ru>]>',
            str(av1.requestqueueelement_set.all()))
        self.assertEqual(p1.record_set.filter(document=av1).first().due_to, datetime.date(year=2018, month=3, day=16))

    def test_ten(self):
        """
        TC 10
        """
        p1 = CustomUser.objects.get(last_name='Afonso')
        d1 = Book.objects.first()
        v = CustomUser.objects.get(last_name='Rama')

        self.login_and_check_out(part_of_mail=1, user=p1, document=d1, day=26)
        p1.record_set.get(document=d1).renew_by_user(p1, date=datetime.date(year=2018, month=3, day=29))
        self.login_and_check_out(part_of_mail=5, user=v, document=d1, day=29)
        v.record_set.get(document=d1).renew_by_user(v, date=datetime.date(year=2018, month=3, day=29))

        self.assertEqual(p1.record_set.filter(document=d1).first().due_to,
                         datetime.date(year=2018, month=4, day=26))
        self.assertEqual(p1.record_set.filter(document=d1).first().document.title, "Introduction to Algorithms")
        self.assertEqual(v.record_set.filter(document=d1).first().due_to, datetime.date(year=2018, month=4, day=5))
        self.assertEqual(v.record_set.filter(document=d1).first().document.title, "Introduction to Algorithms")
