from unittest import result
from urllib.parse import urlparse, parse_qs, unquote

from django.template import Template, Context
from django.test import TestCase

from clickthroughs.templatetags.click_tags import clickthrough
from clickthroughs.models import (
    Campaign,
    CampaignHostname,
    Parameter,
    Platform
)


class ClickthroughTemplateTagTests(TestCase):

    def setUp(self):
        # create platform
        self.platform = Platform.objects.create(name="Test Platform")

        # campaign linked to platform
        self.campaign = Campaign.objects.create(
            name="Test Campaign",
            platform=self.platform,
            start_date=None,
            end_date=None,
        )

        # hostname pointing to campaign
        self.ch = CampaignHostname.objects.create(
            campaign=self.campaign,
            hostname="example.com"
        )

        # parameter linked to platform (not campaign)
        self.param = Parameter.objects.create(
            platform=self.platform,
            key="affiliate_id",
            value="abc123"
        )

        self.campaign.parameters.add(self.param)


    def test_url_tag(self):
        tpl = Template("{% load click_tags %}foo {% clickthrough 'https://example.com/some/page' %} bar")
        rendered = tpl.render(Context())
        self.assertIn("/?to=https%3A%2F%2Fexample.com%2Fsome%2Fpage", rendered)


    def test_campaign_parameters_are_added_to_url(self):
        url = "https://example.com/foo?x=1"
        result = clickthrough(url)

        inner_url = self._get_inner_url(result)

        self.assertIn("affiliate_id=abc123", inner_url)
        self.assertIn("x=1", inner_url)


    def _get_inner_url(self, click_url: str) -> str:
        """Helper to extract the 'to' parameter from a clickthrough URL."""
        parsed = urlparse(click_url)
        params = parse_qs(parsed.query)
        to_url = params.get('to', [None])[0]
        return unquote(to_url) if to_url else ""
