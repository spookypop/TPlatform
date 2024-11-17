from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.views import APIView
import re
from group.models import users
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from TPlatform.token_moduel import get_token
import time
from .serializer import GroupSerializer


# 用户注册
class Register(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # 验证用户是否存在
        is_user = users.objects.filter(username=username)
        if is_user:
            # 用户已经存在
            result = {"status": "10013", "data": {'msg': '用户已存在'}}
            return Response(result, status=status.HTTP_200_OK)
        elif username and password:  # 保存用户
            username = username.strip()
            password_required = re.compile(r"^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{6,18}$")
            if password_required.match(password):
                password = make_password(password)
                users.objects.create(username=username, password=password)
                result = {"status": "10000", "data": {'msg': '注册成功'}}
                return Response(result, status=status.HTTP_200_OK)

            else:
                result = {"status": "10011", "data": {'msg': '密码必须为6-18位，大小写字母和数字的组合'}}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "10012", "data": {'msg': '必填项不能为空'}}
            return Response(result, status=status.HTTP_200_OK)


# 用户登录
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            if users.objects.filter(username=username):  # 查询数据库检查用户名是否存在
                users_result = users.objects.get(username=username)
                password_result = check_password(password, users_result.password)  # 校验输入的密码是否正确
                if password_result:
                    token = get_token(username, 6000)  # 生成用户的token值，并设置token有效期
                    if Token.objects.filter(user_id=users_result.id):  # 用户验证成功后更新数据库的token，首次登录则创建token
                        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        Token.objects.filter(user_id=users_result.id).update(key=token, created=now_time)
                        response = {'username': username, 'token': token}
                        result = {"status": "10000", "data": response}
                        return Response(result, status=status.HTTP_200_OK)
                    else:
                        Token.objects.create(key=token, user_id=users_result.id)
                        response = {'username': username, 'token': token}
                        result = {"status": "10000", "data": response}
                        return Response(result, status=status.HTTP_200_OK)
                else:
                    result = {"status": "20001", "data": {'msg': '账号或密码不正确'}}
                    return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": "20002", "data": {'msg': '用户不存在'}}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "20003", "data": {'msg': '账号或密码不能为空'}}
            return Response(result, status=status.HTTP_200_OK)


# 登出
class Logout(APIView):
    def post(self, request):
        username = request.data.get("username")
        if username:
            user_result = users.objects.get(username=username)
            Token.objects.filter(user_id=user_result.id).delete()
            result = {"status": "10000", "data": {'msg': '用户已退出登录'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "20004", "data": {'msg': '用户不存在'}}
            return Response(result, status=status.HTTP_200_OK)


class LoginUser(APIView):
    def get(self, request):
        current_user = request.session.get('user', None)
        username = current_user['username']
        result = {"status": "100000", "data": {'username': username}}
        return Response(result, status=status.HTTP_200_OK)



class UserList(APIView):
    def get(self, request):
        user_list = users.objects.all()
        username = request.query_params.get("username")
        serialize = GroupSerializer(user_list, many=True)

        if username:
            user = users.objects.filter(username=username)
            user_serializer = GroupSerializer(user, many=True)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serialize.data, status=status.HTTP_200_OK)
