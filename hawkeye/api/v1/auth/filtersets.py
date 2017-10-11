
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from guardian.models import UserObjectPermission

import rest_framework_filters as filters


class UserFilterSet(filters.FilterSet):
    class Meta:
        model = get_user_model()
        fields = {
            'username': ('exact', 'in', 'icontains',),
            'fullname': ('exact', 'in', 'icontains',),
            'owner': ('exact',),
        }

class PermissionFilterSet(filters.FilterSet):
    class Meta:
        model = Permission
        fields = {
            'content_type': ('exact', 'in',),
            'content_type__app_label': ('exact', 'in', 'icontains', ),
            'content_type__model': ('exact', 'in', 'icontains', ),
            'codename': ('exact', 'in', 'icontains', ),
        }
        
class UserObjectPermissionFilterSet(filters.FilterSet):
    class Meta:
        model = UserObjectPermission
        fields = {
            'user': ('exact', 'in',),
            'content_type': ('exact', 'in',),
            'content_type__app_label': ('exact', 'in', 'icontains', ),
            'content_type__model': ('exact', 'in', 'icontains', ),
            'permission': ('exact', 'in',),
            'permission__codename': ('exact', 'in', 'icontains',),
            'object_pk': ('exact', 'in',),
        }