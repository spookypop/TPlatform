from django.db import models


# Create your models here.

class sprints(models.Model):
    sprint_name = models.CharField('迭代名称', max_length=50, unique=True)
    state_choice = ((0, '未开始'), (1, '进行中'), (2, '已结束'))
    state = models.CharField('状态', choices=state_choice, default=0, max_length=20)
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        # 按状态排序
        ordering = ["state", ]


class cases(models.Model):
    app_name = models.CharField('系统/页面/应用', max_length=500)
    module_name = models.CharField('模块名称', max_length=500)
    case_description = models.CharField('用例描述', max_length=500)
    case_data = models.CharField('测试数据', max_length=500, default='')
    sprint_name = models.ForeignKey('sprints', on_delete=models.CASCADE)
    result_choice = ((0, '未执行'), (1, '失败'), (2, '挂起'), (3, '成功'))
    remarks = models.CharField('备注', default='', max_length=500)
    user = models.CharField('执行人', default='', max_length=200)
    result = models.CharField('执行结果', choices=result_choice, default=0, max_length=20)
