from random import choice

from django.contrib.auth.decorators import login_required
from rest_condition import Or
from rest_framework import status
from rest_framework.decorators import detail_route, api_view, parser_classes
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_bulk.generics import BulkModelViewSet

from api.v1.monitor.filtersets import DreamFilterSet
from api.v1.monitor.serializers import DreamSerializer
from authx.permissions import IsAdminUser, IsSuperUser
from monitor.models import Dream, Donor
import xlrd


class DreamViewSet(BulkModelViewSet):
    queryset = Dream.objects.all()
    serializer_class = DreamSerializer
    filter_class = DreamFilterSet
    # permission_classes = (Or(IsAdminUser, IsAuthenticated),)
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsSuperUser()]
        if self.request.method == 'POST':
            return [IsSuperUser()]
        if self.request.method == 'PATCH':
            return [IsSuperUser()]
        else:
            return [AllowAny()]

    @detail_route(
        methods=['POST'],
        url_path='claim',
    )
    def claim(self, request, *args, **kwargs):
        donor_name = request.data.get('donor_name')
        phone_num = request.data.get('phone_num')
        code = request.data.get('code')
        if not donor_name or not phone_num or not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        is_validated = validate_code(request, phone_num, code)
        if not is_validated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        dream = self.queryset[0]
        dream.is_claimed = True

        donor = Donor(name=donor_name, phone=phone_num)
        donor.save()
        dream.donor.add(donor)
        dream.save()
        message = f'【万人圆梦】孩子的愿望:{dream.title}被{donor_name}认领，联系方式:{phone_num}'
        message_to_donor = f'【万人圆梦】尊敬的{donor_name}，感谢您参与“万人圆梦”，工作人员将会尽快与您取得联系。' \
                           f'您也可以直接与工作人员联系，联系人：{dream.contact_person.fullname}，联系人：{dream.contact_person.phone_number}'
        yunpian_send_message(phone_num, message_to_donor)
        yunpian_send_message(dream.contact_person.phone_number, message)
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
def send_code(request):
    phone_num = request.data.get('phone_num')
    if not phone_num:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    code = generate_code()
    yunpian_send_code(code, phone_num)
    request.session[phone_num] = code

    return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
def validate_code(request, phone_num, code):
    if not phone_num or not code:
        return False
    if code == request.session[phone_num]:
        return True
    return False


@api_view(['POST', ])
@parser_classes((MultiPartParser,))
def upload_file(request):
    file = request.FILES.get('template')
    wb = xlrd.open_workbook(file_contents=file.read())
    wb_sheet = wb.sheet_by_index(0)
    dream_list = []
    for rownum in range(1, wb_sheet.nrows):
        row = wb_sheet.row_values(rownum)
        dream = Dream(
            title=row[0],
            person_name=row[1],
            age=row[2],
            person_type=row[3],
            want=row[4],
            reason=row[5],
            local=row[6],
            contact_person=request.user
        )
        dream_list.append(dream)
    Dream.objects.bulk_create(dream_list)
    return Response(status=status.HTTP_200_OK)


def generate_code():
    """
    生成四位数字的验证码
    :return:
    """
    seeds = "1234567890"
    random_str = []
    for i in range(4):
        random_str.append(choice(seeds))
    return "".join(random_str)


def yunpian_send_code(code, phone_num):
    from yunpian_python_sdk.model import constant as YC
    from yunpian_python_sdk.ypclient import YunpianClient

    # 初始化client,apikey作为所有请求的默认值
    clnt = YunpianClient('6e3b47b00f792b1067d05a921b1c1d33')
    param = {YC.MOBILE: phone_num, YC.TEXT: f'【万人圆梦】您的验证码是{code}'}
    r = clnt.sms().single_send(param)
    return r.code()


    # 获取返回结果, 返回码:r.code(),返回码描述:r.msg(),API结果:r.data(),其他说明:r.detail(),调用异常:r.exception()
    # 短信:clnt.sms() 账户:clnt.user() 签名:clnt.sign() 模版:clnt.tpl() 语音:clnt.voice() 流量:clnt.flow()


def yunpian_send_message(send_to, message):
    from yunpian_python_sdk.model import constant as YC
    from yunpian_python_sdk.ypclient import YunpianClient
    if not message or not send_to:
        print('没有通知老师，因为联系人为空')
        return
    # 初始化client,apikey作为所有请求的默认值
    clnt = YunpianClient('6e3b47b00f792b1067d05a921b1c1d33')
    param = {
        YC.MOBILE: send_to,
        YC.TEXT: message
    }
    r = clnt.sms().single_send(param)
    return r.code()
