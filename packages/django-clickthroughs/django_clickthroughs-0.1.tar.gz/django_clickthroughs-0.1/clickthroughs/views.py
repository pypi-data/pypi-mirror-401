from django.http import HttpResponseRedirect
from django.views import View

from .models import Clickthrough


class ClickthroughView(View):
    def get(self, request):

        # TODO: switch to get() throughout
        ip_address = request.META['REMOTE_ADDR']
        session_id = request.session.session_key
        user_agent = request.META['HTTP_USER_AGENT']
        url_to = request.GET.get('to')
        hostname = request.META['HTTP_HOST']
        path_from = request.META['HTTP_REFERER']

        click = Clickthrough()
        click.ip_address = ip_address
        click.session_id = session_id
        click.user_agent = user_agent
        click.url_to = url_to
        click.hostname = hostname
        click.path_from = path_from
        click.save()

        return HttpResponseRedirect(url_to)
