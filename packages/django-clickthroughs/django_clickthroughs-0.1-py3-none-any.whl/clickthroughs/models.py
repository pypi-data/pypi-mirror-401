from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Platform(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='parameters')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    class Meta:
        unique_together = ('platform', 'key')  # ensures no duplicate keys per platform

    def __str__(self):
        return f"{self.key}={self.value} ({self.platform})"


class Campaign(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(default='', null=False, unique=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='campaigns')
    parameters = models.ManyToManyField(Parameter, blank=True, related_name='campaigns')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class CampaignHostname(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='hostnames', on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255)


    def __str__(self):
        return self.hostname


    def clean(self):
        """Ensure no overlapping campaigns for the same hostname."""

        super().clean()

        overlapping = CampaignHostname.objects.filter(
            hostname=self.hostname,
            campaign__start_date__lte=self.campaign.end_date or timezone.datetime.max,
            campaign__end_date__gte=self.campaign.start_date or timezone.datetime.min,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError(
                f"Hostname '{self.hostname}' is already used by another active campaign."
            )


class Clickthrough(models.Model):

    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    session_id = models.CharField(blank=True, null=True, max_length=64, verbose_name='Session ID')
    user_agent = models.TextField(blank=True, null=True)
    url_to = models.URLField(blank=True, null=True, verbose_name='To')
    hostname = models.CharField(blank=True, null=True, max_length=256)
    path_from = models.TextField(blank=True, null=True, verbose_name='From')
