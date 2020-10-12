from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponseForbidden, HttpResponse

import re
from .models import User


# Create your views here.


class RegisterView(View):
    # 用户注册
    def get(self, request):
        """
        用户注册页面
        :param request:
        :return:
        """
        return render(request, 'register.html')

    def post(self, request):
        """
        用户注册业务逻辑
        :param request:
        :return:
        """

        # 接收参数
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        mobile = request.POST.get("mobile")
        allow = request.POST.get("allow")

        # 校验参数
        # 判断参数是否齐全
        if any([username, password, password2, mobile, allow]):
            return HttpResponseForbidden("缺少必填项")

        # 判断用户名是否为5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden("请输入5-20个字符的用户名")

        # 判断密码是否位8-20个字符
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return HttpResponseForbidden("请输入8-20位密码")

        # 判断两次输入密码是否一致
        if password != password2:
            return HttpResponseForbidden("两次输入密码不一致")

        # 判断手机号码是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden("请输入正确手机号码")

        # 判断用户是否勾选了协议
        if allow != "on":
            return HttpResponseForbidden("请勾选用户协议")

        # 保存注册数据
        try:
            User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, "register.html", {"register_errmsg": "用户注册失败"})

        # 响应结果
        return redirect(reverse("contents:index"))
