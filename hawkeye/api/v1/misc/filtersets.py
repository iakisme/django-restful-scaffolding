from django.contrib.contenttypes.models import ContentType

import rest_framework_filters as filters


class ContentTypeFilterSet(filters.FilterSet):
    class Meta:
        model = ContentType
        fields = {
            'app_label': ('exact', 'in',),
            'model': ('exact', 'in', ),
        }