from django.db import models


# Create your models here.
class apiauto(models.Model):
    api_module = models.CharField('模块名称', max_length=500)
    scene = models.CharField('场景描述', max_length=500)
    api_name = models.CharField('接口地址/名称/关键字', max_length=500)
    assertion_choice = ((0, '响应结果包含'), (1, '请求状态码是'))
    assertion_rule = models.CharField('校验规则', choices=assertion_choice, default=0, max_length=20)
    assertion = models.CharField('校验点', default='', max_length=500)
    state_choice = ((0, '未执行'), (1, '通过'), (2, '失败'), (3, '无数据'))
    state = models.CharField('状态', choices=state_choice, default=0, max_length=20)
    result_desc = models.CharField('结果详情', max_length=500, default='')
    # sprint_name = models.ForeignKey('SprintList.sprints', on_delete=models.CASCADE)
    name = models.ForeignKey('SprintList.sprints', on_delete=models.CASCADE, to_field="sprint_name")
