
import threading

from django.core.mail import EmailMultiAlternatives, get_connection, send_mail



def send_mass_status_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), send
    each message to each recipient list. Return the number of emails sent.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user and auth_password are set, use them to log in.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.
    """

    messages = []
    for subject, text, html, from_email, recipient,cc_list in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient,cc=cc_list)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    connection = connection or get_connection(username=user, password=password, fail_silently=False)        
    # import pdb; pdb.set_trace()
    return connection.send_messages(messages)
