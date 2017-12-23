from rest_framework.fields import SerializerMethodField
from rest_framework_bulk.serializers import BulkSerializerMixin, \
    BulkListSerializer

from common.serializers import DynamicFieldsModelSerializer
from monitor.models import Dream
from rest_framework import serializers


class DreamSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):
    # image_url = serializers.SerializerMethodField(allow_null=True)
    donor_num = SerializerMethodField()

    # def get_image_url(self, dream):
    #     photo_url = dream.image.url
    #     return photo_url

    def get_donor_num(self, obj):
        return len(obj.donor.all()) if obj.donor else 0

    class Meta:
        model = Dream
        list_serializer_class = BulkListSerializer
        fields = '__all__'

