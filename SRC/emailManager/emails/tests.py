import json
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from emails.models import *


class EmailDetailViewsTest(TestCase):
    def setUp(self):
        # Create  user
        self.test_user1 = CustomUser.objects.create_user(username='testuser1@email.com', password='1X<ISRUkw+tuK',
                                                         recovery_email="lsh@shs.com",
                                                         phone_number=16722222, )
        self.test_user1.is_active = True
        self.test_user1.save()
        test_user2 = CustomUser.objects.create_user(username='testuser2@email.com', password='2X<ISRUkw+tuK',
                                                    recovery_email="ou@shs.com",
                                                    phone_number=12335222)
        test_user2.is_active = True
        test_user2.save()
        test_email1 = Email.objects.create(author=self.test_user1, subject="test", attachment="False")
        test_email1.save()
        # receiver = EmailReceiver.objects.create(email=test_email1,to=test_user2)
        # receiver.save()
        test_place1_0 = EmailPlaceHolders.objects.create(creator=self.test_user1, place_holder="inbox")
        test_place1_0.save()
        test_place1_1 = EmailPlaceHolders.objects.create(creator=self.test_user1, place_holder="sentbox")
        test_place1_1.save()
        test_place1_2 = EmailPlaceHolders.objects.create(creator=self.test_user1, place_holder="trash")
        test_place1_2.save()
        test_place1_3 = EmailPlaceHolders.objects.create(creator=self.test_user1, place_holder="archive")
        test_place1_3.save()
        test_place1_4 = EmailPlaceHolders.objects.create(creator=self.test_user1, place_holder="test")
        test_place1_4.save()
        map_1 = UserEmailMapped.objects.create(user=self.test_user1, place_holder=test_place1_1, email=test_email1)
        map_1.save()
        map_2 = UserEmailMapped.objects.create(user=self.test_user1, place_holder=test_place1_0, email=test_email1)
        map_2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('detail_email', kwargs={'email_id': 1}))
        self.assertRedirects(response, '/users/login/?next=/emails/detail/1/')

    def test_view_access_logged_in_email_detail(self):
        login = self.client.login(username='testuser1@email.com', password='1X<ISRUkw+tuK')
        login_user = CustomUser.objects.get(username='testuser1@email.com')
        email = Email.objects.get(Q(author=login_user))
        response = self.client.get(reverse('detail_email', kwargs={'email_id': email.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_archive_or_trash_email(self):
        login = self.client.login(username='testuser1@email.com', password='1X<ISRUkw+tuK')
        login_user = CustomUser.objects.get(username='testuser1@email.com')
        email = Email.objects.get(Q(author=login_user))
        # Test adding or removing from archive
        response = self.client.get(reverse('add_email_archive', kwargs={'email_id': email.id}))
        self.assertEqual(response.status_code, 302)
        # Test adding or removing from trash
        response = self.client.get(reverse('delete_email', kwargs={'email_id': email.id}))
        self.assertEqual(response.status_code, 302)


class EmailListViewsTest(TestCase):
    def setUp(self):
        # Create  user
        self.test_user1 = CustomUser.objects.create_user(username='testuser1@email.com', password='1X<ISRUkw+tuK',
                                                         recovery_email="lshswr@shs.com",
                                                         phone_number=189722222, )
        self.test_user1.is_active = True

        self.test_user1.save()

        # create category

    def test_view_create_new_email(self):
        login = self.client.login(username='testuser1@gmz.com', password='1X<ISRUkw+tuK')
        data = {
            'subject': 'test',
            "author": self.test_user1
        }
        # Test forward successfully to an email
        response = self.client.post(reverse('new_email'),
                                    data, follow=True, )
        self.assertEqual(response.status_code, 200)

    def test_view_logged_in_user_search_emails(self):
        login = self.client.login(username='testuser1@email.com', password='1X<ISRUkw+tuK')
        data = json.dumps({'search': 'test'})
        response = self.client.generic('POST', reverse('search'), data)
        self.assertEqual(response.status_code, 405)

    #
    def test_view_creat_new_label(self):
        login = self.client.login(username='testuser1@gmz.com', password='1X<ISRUkw+tuK')
        # Test if it found the integrity error
        data = {'place_holder': 'test1'}
        response = self.client.post(reverse('add_label'), data, follow=True,
                                    )

        self.assertEqual(response.status_code, 200)