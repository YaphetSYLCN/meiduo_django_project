from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse

from .libs.captcha import captcha


# Create your views here.


class ImageCodeView(View):
    """
    图形验证码
    """

    def get(self, request, uuid):
        """
        生成保存响应图形验证码
        :param request:
        :param uuid: 通用唯一识别码
        :return: image/jpg
        """
        # 生成
        text, image = captcha.Captcha().generate_captcha()

        # 保存
        redis_conn = get_redis_connection("verify_code")
        redis_conn.setex("img_{}".format(uuid), 300, text)

        # 响应
        return HttpResponse(image, content_type="image/jpg")
