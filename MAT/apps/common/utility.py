import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.response import Response

from MAT.config.settings.base import EMAIL_HOST_USER


def send_link(email, subject, template, url, *args):
    """A utility to send emails that is reusable"""
    token = ''
    saved_args = locals()
    if saved_args['template'] == 'student_invite_template.html':
        token = saved_args['args'][0]
    from_email, to_email = EMAIL_HOST_USER, email
    site_url = os.getenv('APP_BASE_URL')
    link_url = str(site_url) + \
        url + '{}/'.format(token)
    link_article = url
    message = render_to_string(
        template, {
            'user': to_email,
            'domain': link_url,
            'token': token,
            'username': to_email,
            'link': link_url,
            'link_article': link_article
        })
    send_mail(subject, '', from_email,
            [to_email, ], html_message=message, fail_silently=False)
