from urllib.parse import urlparse, parse_qsl, urlencode

from django import template
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from clickthroughs.models import CampaignHostname


register = template.Library()

@register.simple_tag
def clickthrough(next_url: str) -> str:
    """Generate a clickthrough URL for the given target URL,
    adding any campaign parameters as required.
    """

    # Determine campaign based on hostname
    parsed_url = urlparse(next_url)
    hostname = parsed_url.hostname

    now = timezone.now().date()

    ch = (
        CampaignHostname.objects.select_related('campaign')
        .filter(
            hostname=hostname
        ).filter(
            Q(campaign__start_date__lte=now) | Q(campaign__start_date__isnull=True),
            Q(campaign__end_date__gte=now) | Q(campaign__end_date__isnull=True),
        )
        .first()
    )

    campaign = ch.campaign if ch else None

    if campaign is not None:
        # Add campaign parameters to URL

        params = dict(parse_qsl(parsed_url.query, keep_blank_values=True))

        for p in campaign.parameters.all():
            params[p.key] = p.value

        new_query = urlencode(params, doseq=True)
        next_url = parsed_url._replace(query=new_query).geturl()


    cturl = reverse('clickthroughs:go')

    return cturl + '?' + urlencode({'to': next_url})
