import typing as t
import css_inline
from django.template import loader
from saas_base.settings import saas_settings


def render_mail_messages(template_id: str, context: t.Dict[str, t.Any]) -> t.Tuple[str, str]:
    context.setdefault('site', saas_settings.SITE)
    text: str = loader.render_to_string(f'saas_emails/{template_id}.text', context)
    html: str = loader.render_to_string(f'saas_emails/{template_id}.html', context)
    return text, css_inline.inline(html)
