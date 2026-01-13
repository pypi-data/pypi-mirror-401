from django.test import TestCase
from django.urls import reverse
from clickthroughs.models import Clickthrough

class ClickthroughViewTests(TestCase):
    def test_redirect_logs_click(self):
        target_url = 'https://example.com'

        # TODO: test with various headers missing
        response = self.client.get(
            reverse('clickthroughs:go'), {'to': target_url},
            HTTP_USER_AGENT='TestAgent/1.0',
            HTTP_HOST='example.org',
            HTTP_REFERER='http://foo.bar/',
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], target_url)
        self.assertEqual(Clickthrough.objects.count(), 1)
        self.assertEqual(Clickthrough.objects.first().url_to, target_url) # type: ignore
