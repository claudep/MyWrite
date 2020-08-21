from django.core import mail
from django.test import TestCase

class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'Here is the message.',
            'ghlklkl5@gmail.com', ['lielhanohov@outlook.co.il'],
            fail_silently=False,
        )