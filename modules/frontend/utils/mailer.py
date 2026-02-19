from flask_mailman import EmailMessage
from setup import settings
from flaskr.core.forms import ContactForm
from flask import render_template
import logging

logger = logging.getLogger(__name__)


def send_contact_request_mail(contact_form: ContactForm):
    sender_email = settings.MAIL_USERNAME
    contact_request_dst_email = settings.CONTACT_REQUEST_DST_EMAIL

    html_content = render_template(
        'emails/contact-request.html',
        name=contact_form.name.data,
        email=contact_form.email.data,
        subject=contact_form.subject.data,
        message=contact_form.message.data
    )

    plain_body = f''' Bonjour 📩 Nouveau message via le formulaire de contact
    '''

    msg = EmailMessage(
        subject='Demande de contact depuis le site',
        body=html_content,
        from_email=sender_email,
        to=[contact_request_dst_email]
    )

    msg.content_subtype = "html"

    try:
        msg.send()
        return True
    except Exception as e:
        logger.exception(e)
        return False
