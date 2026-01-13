from django.test import TestCase
from django.core.exceptions import ValidationError

from clickthroughs.models import (
    Clickthrough,
    Campaign,
    CampaignHostname,
    Parameter,
    Platform
)

class ClickthroughModelTests(TestCase):

    def setUp(self):
        self.platform = Platform.objects.create(name="Test Platform")

        self.campaign1 = Campaign.objects.create(
            name="Campaign 1",
            slug="campaign-1",
            platform=self.platform,
            start_date="2024-01-01",
            end_date="2024-12-31",
        )
        self.campaign2 = Campaign.objects.create(
            name="Campaign 2",
            slug="campaign-2",
            platform=self.platform,
            start_date="2024-06-01",
            end_date="2024-12-31",
        )

        self.ch1 = CampaignHostname.objects.create(
            campaign=self.campaign1,
            hostname="overlap.com"
        )

        self.ch2 = CampaignHostname(
            campaign=self.campaign2,
            hostname="overlap.com"
        )


    def test_create_clickthrough(self):
        c = Clickthrough.objects.create(
            ip_address='127.0.0.1',
            url_to='https://example.com',
        )
        self.assertIsNotNone(c.clicked_at)
        self.assertEqual(c.ip_address, '127.0.0.1')
        self.assertEqual(c.url_to, 'https://example.com')


    def test_campaign_hostname_overlap_prevention(self):

        with self.assertRaises(ValidationError) as context:
            self.ch2.clean()

        self.assertIn(
            "Hostname 'overlap.com' is already used by another active campaign.",
            str(context.exception))


    def test_campaign_hostname_overlap_with_self_is_ok(self):

        self.ch2.pk = self.ch1.pk  # Simulate updating the same record
        self.ch2.clean() # Should not raise any exception


class ModelStrTests(TestCase):
    def test_str_methods(self):
        platform = Platform.objects.create(name="Test Platform")
        campaign = Campaign.objects.create(name="Test Campaign", platform=platform)
        ch = CampaignHostname.objects.create(campaign=campaign, hostname="example.com")
        param = Parameter.objects.create(platform=platform, key="key1", value="value1")

        self.assertEqual(str(platform), "Test Platform")
        self.assertEqual(str(campaign), "Test Campaign")
        self.assertEqual(str(ch), "example.com")
        self.assertEqual(str(param), "key1=value1 (Test Platform)")
