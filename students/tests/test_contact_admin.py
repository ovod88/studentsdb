from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse

class ContactAdminFormTests(TestCase):

    fixtures = ['fixture_data.json']

    def test_email_sent(self):
        """Check if email is being sent"""
        # prepare client and login as administrator
        client = Client()
        client.login(username='ovod88', password='taon8888')

        # make form submit
        response = client.post(reverse('contact_admin'), {
            'from_email': 'from@gmail.com',
            'subject': 'test email',
            'message': 'test email message'
        })

        # check if test email backend catched our email to admin
        msg = mail.outbox[0].message()
        self.assertEqual(msg.get('subject'), 'test email')
        self.assertEqual(msg.get('From'), u'from@gmail.com')
        self.assertEqual(msg.get_payload(), 'test email message',)
