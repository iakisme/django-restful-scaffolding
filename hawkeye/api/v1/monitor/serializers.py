from rest_framework_bulk.serializers import BulkSerializerMixin, \
    BulkListSerializer

from common.serializers import DynamicFieldsModelSerializer
from monitor.models import Dream
from rest_framework import serializers


class DreamSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Dream
        list_serializer_class = BulkListSerializer
        fields = '__all__'

    def get_image_url(self, dream):
        photo_url = dream.image.url
        return photo_url
