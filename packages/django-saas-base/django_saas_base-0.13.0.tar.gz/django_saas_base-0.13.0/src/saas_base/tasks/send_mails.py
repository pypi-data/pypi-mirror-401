import typing as t
from django.tasks import task
from django.core.mail import EmailMultiAlternatives


@task
def send_email(
    subject: str,
    recipients: t.List[str],
    text_message: str,
    html_message: t.Optional[str] = None,
    from_email: t.Optional[str] = None,
    headers: t.Optional[t.Dict[str, str]] = None,
    reply_to: t.Optional[str] = None,
):
    mail = EmailMultiAlternatives(
        subject,
        body=text_message,
        from_email=from_email,
        to=recipients,
        headers=headers,
        reply_to=reply_to,
    )
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    return mail.send()
