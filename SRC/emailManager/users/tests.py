from django.test import TestCase, Client
from django.urls import reverse, resolve
from .urls import *
from .models import *
from .views import *
from django.conf import settings


class CustomUserTest(TestCase):
    def setUp(self):
        user_01 = CustomUser(username='zeynabyousefi@email.com', recovery_email="zeynabyousefi1380@gmail.com")
        user_01_p = "0926017616z"
        self.user_01_p = user_01_p
        user_01.set_password(user_01_p)
        user_01.save()
        self.user_01 = user_01
        inbox = EmailPlaceHolders(place_holder="inbox")
        inbox.save()
        sent_box = EmailPlaceHolders(place_holder="sentbox")
        sent_box.save()
        drafts = EmailPlaceHolders(place_holder="drafts")
        drafts.save()
        trash = EmailPlaceHolders(place_holder="trash")
        trash.save()

        print(user_01)

    def test_home_page(self):
        # send GET request.
        # request to the specified url with GET request method.
        response = self.client.get(path='http://127.0.0.1:8000/emails/email-view/')
        self.assertEqual(response.status_code, 302)

    def test_user_exists(self):
        user_count = CustomUser.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        user_exists = CustomUser.objects.filter(username="zeynabyousefi@email.com")
        user_exists_check = user_exists.exists() and user_exists.count() == 1
        self.assertTrue(user_exists_check)
        user_01 = user_exists.first()
        self.assertTrue(user_01.check_password(self.user_01_p))

    def test_login_user_is_true(self):
        data = {"username": 'zeynabyousefi@email.com', "password": self.user_01_p}
        response = self.client.post('/users/login/', data
                                    )
        status = response.status_code
        self.assertEqual(status, 302)
        self.assertRedirects(response, '/emails/email-view/', status_code=302, target_status_code=302)
        # self.assertTemplateUsed(response, 'users/login.html')

    def test_login_use_empty_username_password(self):
        login_account_test_data = {'username': '', 'password': ''}
        # send POST request.
        response = self.client.post(path='/users/login/', data=login_account_test_data)
        self.assertEqual(response.status_code, 200)

    def test_login_username_or_password_not_correct(self):
        login_account_test_data = {'username': 'Admin', 'password': 'qqqqqq'}
        response = self.client.post(path='/users/login/', data=login_account_test_data)
        self.assertEqual(response.status_code,200)


class ContactViewsTest(TestCase):
    def setUp(self):
        # Create  user
        self.test_dict = {}
        self.client = Client()

        self.test_user1 = CustomUser.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK',
                                                         recovery_email="gsh@shs.com",
                                                         phone_number=123222222)
        self.test_user1.is_active = True
        self.test_user1.save()
        self.test_dict.update({"key": self.test_user1.password})
        test_user2 = CustomUser.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD',
                                                    recovery_email="gsh@shsvgsf.com",
                                                    phone_number=123222672)
        self.test_contact1 = Contact.objects.create(owner_contact=self.test_user1, name='test_contact',
                                                    email='zeynabyousefi1380@gmail.com')
        self.test_contact1.save()
        self.test_signature1 = Signature.objects.create(owner=self.test_user1, name='test1', content="testing")
        self.test_signature1.save()

    def test_view_urls_related_to_contacts_exists(self):
        login_user = CustomUser.objects.get(username=self.test_user1)
        log = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        contact = Contact.objects.get(owner_contact=login_user.id)
        response = self.client.get('/users/all-users/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('all_contacts'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('detail_contact', kwargs={'contact_id': contact.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('contact_update', kwargs={'contact_id': contact.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('contact_delete', kwargs={'contact_id': contact.id}))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('all_contacts'))
        self.assertRedirects(response, '/users/login/?next=/all-users/')

    def test_view_works_for_logged_in_user(self):
        log = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        self.assertTrue(log)
        response = self.client.get(reverse('all_contacts'))

        self.assertEqual(str(response.context['user']), self.test_user1.username)

    def test_view_redirect_to_contact_detail_of_the_logged_in_user(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        login_user = CustomUser.objects.get(username='testuser1')
        contact = Contact.objects.get(owner_contact=login_user.id)
        # test if it redirect to the detail view of the log in user
        response = self.client.get(reverse('detail_contact', kwargs={'contact_id': contact.id}))
        self.assertEqual(response.status_code, 200)
        # test if it raise 404 error when the contact dose not exist
        response = self.client.get(reverse('detail_contact', kwargs={'contact_id': 20}))
        self.assertEqual(response.status_code, 404)

    def test_view_logged_in_user_update_its_contact(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        login_user = CustomUser.objects.get(username='testuser1')
        contact = Contact.objects.get(owner_contact=login_user.id)
        response = self.client.get(reverse('contact_update', kwargs={'contact_id': contact.id}))
        # Check we used correct template
        self.assertTemplateUsed(response,'users/update_contact.html')
    #
    def test_view_logged_in_user_delete_its_contact(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        login_user = CustomUser.objects.get(username='testuser1')
        contact = Contact.objects.get(owner_contact=login_user.id)
        response = self.client.get(reverse('contact_delete', kwargs={'contact_id': contact.id}))
        self.assertEqual(response.status_code, 302)
    #
    def test_view_logged_in_user_download_contacts(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('export_contact'))
        self.assertEqual(response.status_code, 200)
