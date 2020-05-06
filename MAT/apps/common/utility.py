import os

from cloudinary.uploader import upload
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import permissions
from rest_framework.response import Response

from MAT.config.settings.base import EMAIL_HOST_USER, env


def send_link(**kwargs):
    """A utility to send emails that is reusable email, subject, template, url, """
    token = kwargs.get('token')
    email = kwargs.get('email')
    subject = kwargs.get('subject')
    url = kwargs.get('url')
    template = kwargs.get('template')

    from_email, to_email = EMAIL_HOST_USER, email
    password = env.str('STUDENTS_PASSWORD')
    base_url = env.str('APP_BASE_URL')

    link = '{0}{1}{2}/'.format(str(base_url), str(url), str(token))

    message = render_to_string(
        template, {
            'user': to_email,
            'token': token,
            'username': to_email,
            'link': link,
            'password': password,
        })
    send_mail(subject, '', from_email,
              [to_email, ], html_message=message, fail_silently=False)


def make_cloudinary_url(image, username):
    """A function to upload images to cloudinary

    Arguments:
        image {[file]} -- The image to upload
        username {[string]} -- username used to name the image url

    Returns:
        [string] -- [The url returned when upload is finished]
    """
    cloudinary_response = upload(
        image, folder=settings.CLOUDINARY_FOLDER, public_id=username, overwrite=True
    )
    secure_url = cloudinary_response["secure_url"]
    return secure_url
