# django-clickthroughs

Logging and reporting for outbound links, with ability to configure in extra
parameters such as affiliate tags.


## Installation notes

 - add `clickthroughs` to `INSTALLED_APPS`
 - add `urls.py` entry (pick your own URL space)
 - run migrations: `python manage.py migrate clickthroughs`


## Usage notes

```
{% load click_tags %}

<a href="{% clickthrough 'https://example.com' %}">Visit Example</a>

```

