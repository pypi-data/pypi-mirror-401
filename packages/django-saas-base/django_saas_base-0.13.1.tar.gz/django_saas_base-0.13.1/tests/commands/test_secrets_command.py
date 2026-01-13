import pytest
from django.test import override_settings
from django.core.management import call_command
from django.core.management.base import CommandError


@override_settings(SAAS_SECRETS_FILE=None)
def test_no_secrets_file():
    with pytest.raises(CommandError, match="SAAS_SECRETS_FILE setting is not set"):
        call_command('secrets', 'list')


@override_settings(SAAS_SECRETS_FILE='.not-exists-secrets')
def test_secrets_list_empty(capsys):
    call_command('secrets', 'list')
    captured = capsys.readouterr()
    assert "No secrets found." in captured.out


def test_list_default_secrets(capsys):
    call_command('secrets', 'list')
    captured = capsys.readouterr()
    assert "turnstile" in captured.out
