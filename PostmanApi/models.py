from django.db import models


class CollectionList(models.Model):
    collection_name = models.CharField('文件名称', default='', max_length=500)
    file_type = models.CharField('文件类型,1是PostmanCollection，2是全局变量，3是环境变量，4是数据csv文件', max_length=20)
    file_name = models.CharField('上传的文件名称', max_length=200)
    file_path = models.CharField(max_length=500)
    upload_time = models.DateTimeField('上传时间', auto_now=True)
