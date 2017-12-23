from django.contrib.contenttypes.models import ContentType

import rest_framework_filters as filters

from monitor.models import Dream


class DreamFilterSet(filters.FilterSet):
    class Meta:
        model = Dream
        fields = {
            'is_claimed': ('exact', 'in', 'icontains'),
            'local': ('exact', 'in', 'icontains'),
            'title': ('icontains',)
        }
