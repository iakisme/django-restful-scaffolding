import base64
from datetime import datetime
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.utils.encoding import smart_text, smart_bytes
from guardian.models import UserObjectPermission
from rest_condition import Or
from rest_framework import status
from rest_framework.decorators import api_view, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import BulkCreateModelMixin
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import obtain_jwt_token, \
    refresh_jwt_token, verify_jwt_token
import json
from api.v1.auth.filtersets import UserFilterSet, PermissionFilterSet, \
    UserObjectPermissionFilterSet
from api.v1.auth.serializers import UserSerializer, UserGroupSerializer, \
    PermissionSerializer, UserObjectPermissionSerializer
from authx.permissions import IsAdminUser, IsSuperUser
from authx.models import User
import time
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
# just a simple wrapper with extra version parameter

@api_view(['POST'])
def test(request):
    return Response({'msg': 'v1 test'})



def jwt_response_special_handling(response, user=None):
    # special handling for login(obtain_xxx) and register on successful jwt response
    # just add an extra info for is_necessary_user_info_filled telling the client to nav to profile page
    if user is None:
        token = response.data.get('token')
        user = __resolve_user(token)
    return response


def __resolve_user(token):
    # a little bit overheaded but just login interface for the time being
    serializer = VerifyJSONWebTokenSerializer(data={'token': token,})
    serializer.is_valid(raise_exception=True)
    return serializer.object.get('user')


@api_view(['POST', ])
def register(request):
    # need to do some transform on this request.data in order to use UserCreationSerializer
    composed_profile = {
        'phone_num': request.data.get('phone_num'),
        'city': request.data.get('city'),
    }
    request.data['profile'] = composed_profile
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response_data = jwt_response_payload_handler(token, user, request)
        return jwt_response_special_handling(
                    Response(response_data, status.HTTP_201_CREATED), user=user
                )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def login(*args, **kwargs):
    response = obtain_jwt_token(*args, **kwargs)
    if status.is_success(response.status_code):
        # according to rest_framework_jwt.utils.jwt_response_payload_handler
        # response.data = {'token': xxxx, ...}
        response = jwt_response_special_handling(response)
    return response


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilterSet
    permission_classes = (Or(IsAdminUser, IsAuthenticated), )

    def create(self, request, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'Error decoding signature.'},status=status.HTTP_400_BAD_REQUEST)
        request.data['owner'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(
        methods=['get'],
        url_path='user-info'
    )
    def current_user_info(self, request):
        # may go with groups
        serializer = UserGroupSerializer(request.user)
        return Response(serializer.data)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilterSet
    permission_classes = (Or(IsAdminUser, IsSuperUser), )


class UserObjectPermissionViewSet(ModelViewSet):
    queryset = UserObjectPermission.objects.all()
    serializer_class = UserObjectPermissionSerializer
    filter_class = UserObjectPermissionFilterSet
    permission_classes = (Or(IsAdminUser, IsSuperUser), )
    
    @list_route(
        methods=['post'],
        url_path='grant',
        permission_classes = (Or(IsAdminUser, IsSuperUser), )
    )
    @atomic
    def grant_permissions(self, request):
        user_id = request.data.get('user') or request.data.get('user_id') or ''
        content_type_id = request.data.get('content_type') or request.data.get('content_type_id') or ''
        permission_id = request.data.get('permission') or request.data.get('permission_id') or ''
        user = get_object_or_404(get_user_model(), id=user_id)
        content_type = get_object_or_404(ContentType, id=content_type_id)
        permission = get_object_or_404(Permission, id=permission_id)
        UserObjectPermission.objects.filter(user=user, 
                content_type=content_type, permission=permission).delete()
        
        object_pks = request.data.get('object_pks') or []
        objs = content_type.get_all_objects_for_this_type(id__in=object_pks)
        items = []
        for obj in objs:
            items.append(
                UserObjectPermission(user=user, 
                                     content_type=content_type, 
                                     permission=permission,
                                     object_pk=obj.id)
            )
        UserObjectPermission.objects.bulk_create(items)
        
        return Response(status=status.HTTP_204_NO_CONTENT)



