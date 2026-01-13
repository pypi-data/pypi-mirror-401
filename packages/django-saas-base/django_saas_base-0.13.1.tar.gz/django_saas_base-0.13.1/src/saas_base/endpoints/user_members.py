from rest_framework.request import Request
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from saas_base.drf.filters import IncludeFilter, ChoiceFilter, CurrentUserFilter
from saas_base.drf.views import AuthenticatedEndpoint
from saas_base.models import Member
from saas_base.serializers.member import UserMembershipSerializer

__all__ = [
    'UserMemberListEndpoint',
    'UserMemberItemEndpoint',
]


class UserMemberListEndpoint(ListModelMixin, AuthenticatedEndpoint):
    serializer_class = UserMembershipSerializer
    queryset = Member.objects.select_related('tenant').all()
    filter_backends = [CurrentUserFilter, IncludeFilter, ChoiceFilter]
    resource_scopes = ['user', 'user:member']

    choice_filter_fields = ['status']
    include_select_related_fields = ['role']
    include_prefetch_related_fields = ['groups', 'permissions', 'groups__permissions']

    def get(self, request: Request, *args, **kwargs):
        """List all the current user's tenants."""
        return self.list(request, *args, **kwargs)


class UserMemberItemEndpoint(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, AuthenticatedEndpoint):
    serializer_class = UserMembershipSerializer
    queryset = Member.objects.all()
    filter_backends = [CurrentUserFilter]
    resource_scopes = ['user', 'user:member']

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
