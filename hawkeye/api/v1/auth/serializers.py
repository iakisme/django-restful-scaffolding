from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from guardian.models import UserObjectPermission
from rest_framework.fields import SerializerMethodField

from common.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers

class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        #exclude = ('password', )

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.fullname = validated_data['fullname']
        user.set_password(validated_data['password'])
        user.is_superuser = validated_data['is_superuser']
        user.is_staff = validated_data['is_staff']
        user.is_admin = validated_data['is_admin']
        user.owner = validated_data['owner']
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                if not 'old_password' in self.initial_data or not instance.check_password(self.initial_data["old_password"]):
                    raise serializers.ValidationError({"error_message": "旧密码错误"})
                else:
                    instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserGroupSerializer(DynamicFieldsModelSerializer):
    groups = SerializerMethodField()

    class Meta:
        model = get_user_model()
        exclude = ('password', )

    def get_groups(self, obj):
        # empty list for the time being
        return []


class PermissionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UserObjectPermissionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserObjectPermission
        fields = '__all__'

# class UserObjectPermissionSerializer(DynamicFieldsModelSerializer):
#     content_object = GenericRelatedField({
#         Database: DatabaseSerializer(),
#     })
#     
#     class Meta:
#         model = UserObjectPermission
#         fields = '__all__'