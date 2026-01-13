import warnings
from saas_base.rules import Rule, BlockedEmailDomains, Turnstile, AvoidTooManyDots as TooManyDots

__all__ = [
    'Rule',
    'BlockedEmailDomains',
    'TooManyDots',
    'Turnstile',
]

warnings.warn('Use saas_base.rules instead', DeprecationWarning)
