from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class users(AbstractUser):  # 继承Django内置的用户类，可自定义字段
    # 邮件字段暂未用到，可设置为非必填
    email = models.EmailField('邮箱', max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now=True)
    last_login = models.DateTimeField('最后一次登录', auto_now=True)


