import warnings
from saas_base.ipware import get_client_ip

__all__ = ['get_client_ip']

warnings.warn('Use saas_base.ipware instead', DeprecationWarning)
