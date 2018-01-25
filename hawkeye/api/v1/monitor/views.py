import io
from random import choice

import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import detail_route, api_view, parser_classes
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_bulk.generics import BulkModelViewSet

from api.v1.monitor.filtersets import DreamFilterSet
from api.v1.monitor.serializers import DreamSerializer
from authx.permissions import IsAdminUser, IsSuperUser
from monitor.models import Dream, Donor, scramble_uploaded_filename
import xlrd
from PIL import Image


class DreamViewSet(BulkModelViewSet):
    queryset = Dream.objects.all()
    serializer_class = DreamSerializer
    filter_class = DreamFilterSet

    # permission_classes = (Or(IsAdminUser, IsAuthenticated),)
    # parser_classes = (JSONParser,)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsSuperUser()]
        if self.request.method == 'POST' and self.action != 'claim':
            return [IsSuperUser()]
        if self.request.method == 'PATCH':
            return [IsSuperUser()]
        else:
            return [AllowAny()]

    @detail_route(
        methods=['POST'],
        url_path='claim',
        parser_classes=[JSONParser, ]
    )
    def claim(self, request, *args, **kwargs):
        donor_name = request.data.get('donor_name')
        phone_num = request.data.get('phone_num')
        code = request.data.get('code')
        dream = self.get_object()
        if dream.is_claimed is True:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not donor_name or not phone_num or not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        is_validated = validate_code(request, phone_num, code)
        if not is_validated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        dream.is_claimed = True
        dream.image_url = 'static/photos/default_img2.jpg'
        donor = Donor(name=donor_name, phone=phone_num)
        donor.save()
        dream.donor.add(donor)
        dream.save()
        title = dream.title
        title = title[:8]
        full_name = dream.contact_name
        phone_number = dream.contact_phone
        message = f'【万人圆梦】亲爱的{full_name}，{dream.person_name}的微心愿已经被{donor_name}认领，联系方式:{phone_num}。希望您在24小时内与微心愿认领人{donor_name}取得联系，并做好对接工作。（共青团宁波市委，联系电话：89186690）'

        message_to_donor = f'【万人圆梦】尊敬的{donor_name}，感谢您参与“2018年宁波市青少年万人圆梦行动微心愿认领活动”，微心愿联系人（一般为困难青少年所在的乡镇街道团干部或所在学校的老师）将会尽快与您取得联系，您也可以直接与微心愿联系人联系，共同商定圆梦方式，如您不方便亲自圆梦，可将您的爱心物资快递到微心愿联系人所在单位，由他们替您将关爱及时送到困难青少年手中。微心愿联系人：{full_name}，联系电话：{int(phone_number)}（共青团宁波市委）'
        yunpian_send_message(int(phone_num), message_to_donor)
        if not dream.contact_phone:
            return Response(status=status.HTTP_200_OK)
        yunpian_send_message(int(dream.contact_phone), message)
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


def validate_code(request, phone_num, code):
    if not phone_num or not code:
        return False
    if code == request.session[phone_num]:
        return True
    return False


@api_view(['POST', ])
@parser_classes((MultiPartParser,))
@login_required
def upload_image(request):
    try:
        file = request.FILES.get('image')
        file_name = scramble_uploaded_filename('1', file.name)
        img = Image.open(file).save(f'static/{file_name}')
    except Exception as e:
        return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"image_url": file_name}, status=status.HTTP_200_OK)


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
            local=row[0],
            person_name=row[1],
            sex=row[2],
            title=row[3],
            reason=row[4],
            contact_name=row[5],
            contact_phone=row[6]
        )
        dream_list.append(dream)
    Dream.objects.bulk_create(dream_list)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', ])
def export_file(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, '所在地')
    worksheet.write(0, 1, '姓名')
    worksheet.write(0, 2, '性别')
    worksheet.write(0, 5, '微心愿')
    worksheet.write(0, 6, '许愿理由')
    worksheet.write(0, 7, '联系人')
    worksheet.write(0, 8, '联系电话')

    dream_list = list(Dream.objects.filter(is_claimed=False))
    for i, dream in enumerate(dream_list):
        worksheet.write(i+1, 0, dream.local)
        worksheet.write(i+1, 1, dream.person_name)
        worksheet.write(i+1, 2, dream.sex)
        worksheet.write(i+1, 5, dream.title)
        worksheet.write(i+1, 6, dream.reason)
        worksheet.write(i+1, 7, dream.contact_name)
        worksheet.write(i+1, 8, dream.contact_phone)
        workbook.close()
        output.seek(0)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="test.xlsx"'
        response.write(output.read())
        # response.write(output.read())
        return response

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
        YC.MOBILE: str(send_to),
        YC.TEXT: message
    }
    r = clnt.sms().single_send(param)
    return r.code()
