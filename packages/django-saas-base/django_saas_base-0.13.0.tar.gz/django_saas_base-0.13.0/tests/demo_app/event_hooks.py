from django.dispatch import receiver
from saas_base.signals import mail_queued
from saas_base.utils.mail_templates import render_mail_messages
from saas_base.tasks.send_mails import send_email


@receiver(mail_queued)
def send_mail_async(sender, template_id, subject, recipients, context, **kwargs):
    text_message, html_message = render_mail_messages(template_id, context)
    send_email.enqueue(
        subject=str(subject),
        recipients=recipients,
        text_message=text_message,
        html_message=html_message,
    )
