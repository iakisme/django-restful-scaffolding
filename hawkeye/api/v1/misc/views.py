from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework_bulk.generics import BulkModelViewSet

from api.v1.misc.filtersets import ContentTypeFilterSet
from api.v1.misc.serializers import ContentTypeSerializer


class ContentTypeViewSet(BulkModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    filter_class = ContentTypeFilterSet
    search_fields = ('app_label', 'model')
    permission_classes = (IsAuthenticated, )
