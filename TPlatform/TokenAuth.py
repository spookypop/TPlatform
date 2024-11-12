from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotAuthenticated
from rest_framework.authtoken.models import Token
from TPlatform.token_moduel import get_token, out_token


class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')  # 获取前端传的token
        key = request.data.get('username')
        token_obj = out_token(key, token)
        # token_obj=Token.objects.filter(key=token) # 校验是否有该token
        if token_obj:
            return
        else:
            raise NotAuthenticated("用户未登录")
