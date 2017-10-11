from django.contrib.contenttypes.models import ContentType
from rest_framework_bulk.serializers import BulkSerializerMixin, \
    BulkListSerializer

from common.serializers import DynamicFieldsModelSerializer


class ContentTypeSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):
    class Meta:
        model = ContentType
        list_serializer_class = BulkListSerializer
        fields = '__all__'