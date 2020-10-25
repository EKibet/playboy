from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from MAT.config.settings.base import EMAIL_FROM

logger = get_task_logger(__name__)

@shared_task
def send_email_utility(**kwargs):
    """
    A utility for sending emails
    all args should be kwargs
    required kwargs - recipient_email,subject,template
    optional kwargs - plain_text_message,cc_recipients,template_variables
    --------------------example----------------------------------
    send_email_utility(recipient_email=email,subject=subject,template=template,cc_recipients=None,template_variables= {
                    'username': student_name,
                    'attendance': attendance,
                    'ips': ips,
                    'improvements': reason,
                })
    """
    from_email = EMAIL_FROM
    logger.info("EMAIL_FROM is ",EMAIL_FROM)

    to_email = kwargs.get('recipient_email')
    subject = kwargs.get('subject')
    template = kwargs.get('template')
    plain_text_message = kwargs.get('plain_text_message') #optional
    cc_recipients = kwargs.get('cc_recipients') #optional
    template_variables = kwargs.get('template_variables') #optional

    html_message = render_to_string(
                template, template_variables)

    msg = EmailMultiAlternatives(subject, plain_text_message, from_email, [to_email],cc=cc_recipients)
    msg.attach_alternative(html_message, "text/html")
    msg.send()
