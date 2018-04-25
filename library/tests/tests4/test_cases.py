from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.test import TestCase, RequestFactory

from library.forms import AddCopies
from library.models.request_queue import RequestQueueElement
from library.models.record import Record
from library.models.documents import *
from library.models.author import Author
from django.test.client import RequestFactory
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from library.views import add_copies, remove_copies, document_outstanding_request, search_by_word, search_documents
from login.forms import CustomUserCreationForm
from login.models import CustomUser
from login.views import add_user


class TestCases(TestCase):
    @classmethod
    def setUpTestData(cls):

        #Create authors and documents
        #
        #
        authors_first_book = [
            Author.objects.create(first_name='Thomas H.', last_name='Cormen'),
            Author.objects.create(first_name='Charles E.', last_name='Leiserson'),
            Author.objects.create(first_name='Ronald L.', last_name='Rivest'),
            Author.objects.create(first_name='Clifford', last_name='Stein'),
        ]
        authors_second_book = [
            Author.objects.create(first_name="Niklaus", last_name="Wirth")
        ]

        authors_third_book = [
            Author.objects.create(first_name ="Donald E.", last_name ="Knuth")
        ]
        tags_first_book =  [
            Tag.objects.create(name="Algorithms"), Tag.objects.create(name="Data Structures"),
            Tag.objects.create(name="Complexity"), Tag.objects.create(name='Computational Theory')

        ]
        tags_second_book = [
            Tag.objects.create(name="Algorithms"), Tag.objects.create(name="Data Structures"),
            Tag.objects.create(name="Search Algorithms"), Tag.objects.create(name = "Pascal")
        ]
        tags_third_book = [
            Tag.objects.create(name="Algorithms"), Tag.objects.create(name="Combinatorial Algorithms"),
            Tag.objects.create(name="Recursion")
        ]
        d1 = Book.objects.create_book(
            title='Introduction to Algorithms',
            publisher='MIT Press',
            edition=3,
            year=2009,
            is_bestseller=False,
            authors=authors_first_book,
            price=5000,
            reference=False,
        )
        d1.tags.set(tags_first_book)

        d2 = Book.objects.create_book(
            title='Algorithms + Data Structures = Programs',
            publisher='Prentice Hall PTR',
            edition=1,
            year=1978,
            is_bestseller=False,
            authors=authors_second_book,
            price=5000,
            reference=False,
        )
        d2.tags.set(tags_second_book)

        d3 = Book.objects.create_book(
            title='The Art of Computer Programming',
            publisher='Addison Wesley Longman Publishing Co., Inc',
            edition=3,
            year=1997,
            is_bestseller=False,
            authors=authors_third_book,
            price=5000,
            reference=False,
        )
        d3.tags.set(tags_third_book)
        #Create users and group
        #
        #

        group_faculty = Group.objects.create(name='Faculty')
        group_students = Group.objects.create(name="Students")
        group_visiting_profs = Group.objects.create(name="Visiting Professors")
        group_librarian_Priv1 = Group.objects.create(name= "Librarians (Priv1)")
        group_librarian_Priv2= Group.objects.create(name="Librarians (Priv2)")
        group_librarian_Priv3 = Group.objects.create(name="Librarians (Priv3)")
        perm1 = Permission.objects.get(
            codename='change_document',

        )
        perm2 = Permission.objects.get(
            codename='add_document'
        )
        perm3 = Permission.objects.get(
            codename='delete_document'
        )

        group_librarian_Priv1.permissions.add(perm1)
        group_librarian_Priv2.permissions.add(perm1, perm2)
        group_librarian_Priv3.permissions.add(perm1,perm2,perm3)



        #first user
        p1 = CustomUser.objects.create_user(
            email="p1@mail.ru", first_name="Sergey", last_name="Afonso", address="Via Margutta, 3",
            phone_number='30001', password='temporary'
        )

        p1.groups.add(group_faculty)
        p1.subtype = 'Professors'
        p1.save()

        # second user
        p2 = CustomUser.objects.create_user(
            email="p2@mail.ru", first_name="Nadia", last_name="Teixerina", address="Via Scara, 13",
            phone_number='30002', password='temporary'
        )
        p2.groups.add(group_faculty)
        p2.subtype = 'Professors'
        p2.save()

        # third user
        p3 = CustomUser.objects.create_user(
            email="p3@mail.ru", first_name="Elvira", last_name="Espindola", address="Via del Corso, 22",
            password='temporary',
            phone_number='30003'
        )
        p3.groups.add(group_faculty)
        p3.subtype = 'Professors'
        p3.save()

        # 4th user
        s = CustomUser.objects.create_user(
            email="p4@mail.ru", first_name="Andrey", last_name="Velo", address="Avenida Mazatlan 250",
            password='temporary',
            phone_number='30004'
        )
        s.groups.add(group_students)
        s.subtype = 'Students'
        s.save()  # ПОЧЕМУ АНДРЕЯ ЗОВУТ ЭЛЬВИРА БЛЯДЬ

        # 5th user
        v = CustomUser.objects.create_user(
            email="p5@mail.ru", first_name="Veronika", last_name="Rama", address="Stret Atocha, 27",
            password='temporary',
            phone_number='30005'
        )
        v.groups.add(group_visiting_profs)
        v.subtype = 'Visiting Professors'
        v.save()


        # liiiiibrarian
        lib = CustomUser.objects.create_user(
            email="lib@mail.ru", first_name="Librarian_first_name", last_name="Librarian_last_name",
            address="Innopolis, 1", phone_number='3000234'
        )
        #admin

        admin = CustomUser.objects.create_superuser(
            email="adm@mail.ru", first_name="Admin_first_name", last_name="Admin_last_name",
            address="Innopolis, 1", phone_number='3000234', password="qwertyuiop"
        )

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

    def test_one(self):
        """
        TC 01
        """
        try:
            admin2 = CustomUser.objects.create_superuser(
                email="adm2@mail.ru", first_name="Admin_first_name", last_name="Admin_last_name",
                address="Innopolis, 1", phone_number='3000234', password="qwertyuiop")
            self.fail("My message here")

        except ValidationError:
            self.assertTrue(True)

    def test_two(self):
        """
        TC 02
        """
        admin = CustomUser.objects.get(email='adm@mail.ru')
        data = {
            "email": "lib1@lib.com",
            "first_name": "lib11",
            "last_name": "lib21",
            "phone_number": "0000",
            "address": "Address",
            "subtype": "Librarians (Priv1)",
            "password1": "temporary",
            "password2": "temporary"
        }
        request = HttpRequest()
        request.method = 'POST'
        request.POST = data
        request.user = admin
        add_user(request)

        data = {
            "email": "lib2@lib.com",
            "first_name": "lib12",

            "last_name": "lib22",
            "phone_number": "0000",
            "address": "Address",
            "subtype": "Librarians (Priv2)",
            "password1": "temporary",
            "password2": "temporary"
        }
        form = CustomUserCreationForm(data, caller_is_admin=True)
        form.save()
        data = {
            "email": "lib3@lib.com",
            "first_name": "lib13",
            "last_name": "lib23",
            "phone_number": "0000",
            "address": "Address",
            "subtype": "Librarians (Priv3)",
            "password1": "temporary",
            "password2": "temporary"
        }
        form = CustomUserCreationForm(data, caller_is_admin=True)
        form.save()

        self.assertTrue(len(CustomUser.objects.filter(last_name='lib21').all()) == 1)
        self.assertTrue(len(CustomUser.objects.filter(last_name='lib22').all()) == 1)
        self.assertTrue(len(CustomUser.objects.filter(last_name='lib23').all()) == 1)

    def test_three(self):
        """
        TC 03
        """
        self.test_two()

        #Test 3
        document = Document.objects.get(title='Introduction to Algorithms')
        previous_number_d1 = document.get_number_of_available_copies()
        document = Document.objects.get(title='Algorithms + Data Structures = Programs')
        previous_number_d2 = document.get_number_of_available_copies()
        document = Document.objects.get(title='Algorithms + Data Structures = Programs')
        previous_number_d3 = document.get_number_of_available_copies()

        try:
            user = CustomUser.objects.get(email='lib1@lib.com')

            document = Document.objects.get(title='Introduction to Algorithms')
            request = HttpRequest()
            request.method = 'POST'
            request.POST = {
                'number_of_copies': 12
            }
            request.user = user
            add_copies(request, document.id)

            document = Document.objects.get(title='Algorithms + Data Structures = Programs')
            request = HttpRequest()
            request.method = 'POST'
            request.POST = {
                'number_of_copies': 12
            }
            request.user = user
            add_copies(request, document.id)

            document = Document.objects.get(title='The Art of Computer Programming')
            request = HttpRequest()
            request.method = 'POST'
            request.POST = {
                'number_of_copies': 12
            }
            request.user = user
            add_copies(request, document.id)

        except KeyError:
            document = Document.objects.get(title='Introduction to Algorithms')
            self.assertTrue(document.get_number_of_available_copies() == previous_number_d1)

            document = Document.objects.get(title='The Art of Computer Programming')
            self.assertTrue(document.get_number_of_available_copies() == previous_number_d2)

            document = Document.objects.get(title='Algorithms + Data Structures = Programs')
            self.assertTrue(document.get_number_of_available_copies() == previous_number_d3)





    def test_four(self):
        """
        TC 04
        """
        self.test_two()
        #Test 4

        user = CustomUser.objects.get(email='lib2@lib.com')

        document = Document.objects.get(title='Introduction to Algorithms')
        previous_number = document.get_number_of_available_copies()
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'number_of_copies': 3
        }
        request.user = user
        add_copies(request, document.id)
        self.assertTrue(document.get_number_of_available_copies() == previous_number+3)

        document = Document.objects.get(title='Algorithms + Data Structures = Programs')
        previous_number = document.get_number_of_available_copies()
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'number_of_copies': 3
        }
        request.user = user
        add_copies(request, document.id)
        self.assertTrue(document.get_number_of_available_copies() == previous_number+3)

        document = Document.objects.get(title='The Art of Computer Programming')
        previous_number = document.get_number_of_available_copies()
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'number_of_copies': 3
        }
        request.user = user
        add_copies(request, document.id)
        self.assertTrue(document.get_number_of_available_copies() == previous_number+3)

    def test_five(self):
        """
        TC 05
        """
        self.test_four()
        user = CustomUser.objects.get(email='lib3@lib.com')

        document = Document.objects.get(title='Introduction to Algorithms')
        previous_number = document.get_number_of_available_copies()
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            'number_of_copies': 1
        }
        request.user = user
        remove_copies(request, document.id)
        self.assertTrue(document.get_number_of_available_copies() == 2)


    def test_six(self):
        """
        TC 06
        """
        self.test_four()
        p1 = CustomUser.objects.get(email='p1@mail.ru')
        p2 = CustomUser.objects.get(email='p2@mail.ru')
        p3 = CustomUser.objects.get(email='p3@mail.ru')
        s = CustomUser.objects.get(email='p4@mail.ru')
        v = CustomUser.objects.get(email='p5@mail.ru')
        d3 = Document.objects.get(title='The Art of Computer Programming')
        self.login_and_check_out(part_of_mail=1, user=p1, document=d3)
        self.login_and_check_out(part_of_mail=2, user=p2, document=d3)
        self.login_and_check_out(part_of_mail=3, user=p3, document=d3)
        self.login_and_check_out(part_of_mail=4, user=s, document=d3)
        self.login_and_check_out(part_of_mail=5, user=v, document=d3)
        try:
            user = CustomUser.objects.get(email='lib1@lib.com')
            request = HttpRequest()
            request.user = user
            d3 = Document.objects.get(title='The Art of Computer Programming')
            document_outstanding_request(request, d3.id)
            self.fail(msg="Error")
        except KeyError:
            pass



    def test_seven(self):
        """
        TC 07
        """
        self.test_four()
        p1 = CustomUser.objects.get(email='p2@mail.ru')
        p2 = CustomUser.objects.get(email='p2@mail.ru')
        p3 = CustomUser.objects.get(email='p3@mail.ru')
        s = CustomUser.objects.get(email='p4@mail.ru')
        v = CustomUser.objects.get(email='p5@mail.ru')
        d3 = Document.objects.get(title='The Art of Computer Programming')
        self.login_and_check_out(part_of_mail=1, user=p1, document=d3)
        self.login_and_check_out(part_of_mail=2, user=p2, document=d3)
        self.login_and_check_out(part_of_mail=3, user=p3, document=d3)
        self.login_and_check_out(part_of_mail=4, user=s, document=d3)
        self.login_and_check_out(part_of_mail=5, user=v, document=d3)
        try:
            user = CustomUser.objects.get(email='lib1@lib.com')
            request = HttpRequest()
            request.user = user
            d3 = Document.objects.get(title='The Art of Computer Programming')
            document_outstanding_request(request, d3.id)
            self.fail(msg="Error")
        except KeyError:
            pass



    def test_eight(self):
        """
        TC 08
        """
        import ast

        def user_target_property(user):
            return user['email']

        def record_target_property(record):
            return Document.objects.get(pk=record['document_id']).title

        target_property_mappings = {
            'user': user_target_property,
            'record': record_target_property
        }

        def change_message_to_dict(change_message):
            return ast.literal_eval(change_message)

        self.test_six()
        log_list = [
            {'target': 'lib1@lib.com', 'action': 1},
            {'target': 'lib1@lib.com', 'action': 2},
            {'target': 'lib2@lib.com', 'action': 1},
            {'target': 'lib2@lib.com', 'action': 2},
            {'target': 'lib3@lib.com', 'action': 1},
            {'target': 'lib3@lib.com', 'action': 2},
            {'target': 'Introduction to Algorithms', 'action': 1},
            {'target': 'Introduction to Algorithms', 'action': 1},
            {'target': 'Introduction to Algorithms', 'action': 1},
            {'target': 'Algorithms + Data Structures = Programs', 'action': 1},
            {'target': 'Algorithms + Data Structures = Programs', 'action': 1},
            {'target': 'Algorithms + Data Structures = Programs', 'action': 1},
            {'target': 'The Art of Computer Programming', 'action': 1},
            {'target': 'The Art of Computer Programming', 'action': 1},
            {'target': 'The Art of Computer Programming', 'action': 1},
            {'target': 'p1@mail.ru', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'p2@mail.ru', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'p3@mail.ru', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'p4@mail.ru', 'action': 2},
            {'target': 'p5@mail.ru', 'action': 2}
        ]
        log_entries = LogEntry.objects.order_by('action_time').all()[36:]

        def get_target_property_value_by_idx(idx):
            dct = change_message_to_dict(log_entries[idx].change_message)
            for prop_type in target_property_mappings.keys():
                prop_value_getter = target_property_mappings[prop_type]
                try:
                    return prop_value_getter(dct)
                except:
                    pass


        for i in range(len(log_list)):
            self.assertEqual(
                log_list[i]['action'],
                log_entries[i].action_flag
            )
            prop_value = get_target_property_value_by_idx(i)
            self.assertTrue(log_list[i]['target'] in prop_value)

    def test_nine(self):
        """
        TC 09
        """
        import ast

        def user_target_property(user):
            return user['email']

        def record_target_property(record):
            return Document.objects.get(pk=record['document_id']).title

        target_property_mappings = {
            'user': user_target_property,
            'record': record_target_property
        }

        def change_message_to_dict(change_message):
            return ast.literal_eval(change_message)

        self.test_six()
        log_list = [
            {'target': 'lib1@lib.com', 'action': 1},
            {'target': 'lib1@lib.com', 'action': 2},
            {'target': 'lib2@lib.com', 'action': 1},
            {'target': 'lib2@lib.com', 'action': 2},
            {'target': 'lib3@lib.com', 'action': 1},
            {'target': 'lib3@lib.com', 'action': 2},
            {'target': 'Introduction to Algorithms', 'action': 1},
            {'target': 'Introduction to Algorithms', 'action': 1},
            {'target': 'Introduction to Algorithms', 'action': 1},
            {'target': 'Algorithms + Data Structures = Programs', 'action': 1},
            {'target': 'Algorithms + Data Structures = Programs', 'action': 1},
            {'target': 'Algorithms + Data Structures = Programs', 'action': 1},
            {'target': 'The Art of Computer Programming', 'action': 1},
            {'target': 'The Art of Computer Programming', 'action': 1},
            {'target': 'The Art of Computer Programming', 'action': 1},
            {'target': 'p1@mail.ru', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'p2@mail.ru', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'p3@mail.ru', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'The Art of Computer Programming', 'action': 2},
            {'target': 'p4@mail.ru', 'action': 2},
            {'target': 'p5@mail.ru', 'action': 2}
        ]
        log_entries = LogEntry.objects.order_by('action_time').all()[36:]

        def get_target_property_value_by_idx(idx):
            dct = change_message_to_dict(log_entries[idx].change_message)
            for prop_type in target_property_mappings.keys():
                prop_value_getter = target_property_mappings[prop_type]
                try:
                    return prop_value_getter(dct)
                except:
                    pass

        for i in range(len(log_list)):
            self.assertEqual(
                log_list[i]['action'],
                log_entries[i].action_flag
            )
            prop_value = get_target_property_value_by_idx(i)
            self.assertTrue(log_list[i]['target'] in prop_value)

    def test_ten(self):
        """
        TC 10
        """
        user = CustomUser.objects.filter(email="p5@mail.ru")
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            "title": 'Introduction to Algorithms',
            "authors": "",
            "tags": "",
            "available": "",
            "taken": ''
        }
        request.user = user
        response = search_documents(request)

        self.assertTrue(b'Introduction to Algorithms' in response.content)

    def test_eleven(self):
        """
        TC 11
        """

        user = CustomUser.objects.filter(email="p5@mail.ru")
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            "title": 'Algorithms',
            "authors": "",
            "tags": "",
            "available": "",
            "taken": ''
        }
        request.user = user
        response = search_documents(request)

        self.assertTrue(b'Introduction to Algorithms' in response.content)
        self.assertTrue(b'Algorithms + Data Structures = Programs' in response.content)

    def test_twelve(self):
        """
        TC 12
        """
        user = CustomUser.objects.filter(email="p5@mail.ru")
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            "title": '',
            "authors": "",
            "tags": "Algorithms",
            "available": "",
            "taken": ''
        }
        request.user = user
        response = search_documents(request)

        self.assertTrue(b'Introduction to Algorithms' in response.content)
        self.assertTrue(b'Algorithms + Data Structures = Programs' in response.content)
        self.assertTrue(b'The Art of Computer Programming' in response.content)

    def test_thirteen(self):
        """
        TC 13
        """
        user = CustomUser.objects.filter(email="p5@mail.ru")
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            "title": 'Algorithms AND Programming',
            "authors": "",
            "tags": "",
            "available": "",
            "taken": ''
        }
        request.user = user
        response = search_documents(request)

        self.assertTrue(b'Introduction to Algorithms' not in response.content)
        self.assertTrue(b'Algorithms + Data Structures = Programs' not in response.content)
        self.assertTrue(b'The Art of Computer Programming' not in response.content)

    def test_fourteen(self):
        """
        TC 14
        """
        user = CustomUser.objects.filter(email="p5@mail.ru")
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {
            "title": 'Algorithms OR Programming',
            "authors": "",
            "tags": "",
            "available": "",
            "taken": ''
        }
        request.user = user
        response = search_documents(request)

        self.assertTrue(b'Introduction to Algorithms' in response.content)
        self.assertTrue(b'Algorithms + Data Structures = Programs' in response.content)
        self.assertTrue(b'The Art of Computer Programming' in response.content)












