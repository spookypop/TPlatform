from django.db import models


# Create your models here.
class ui_auto(models.Model):
    ui_name = models.CharField('Ui自动化场景名称', max_length=500)
    state_choice = ((0, '未执行'), (1, '通过'), (2, '失败'))
    state = models.CharField('运行结果', choices=state_choice, max_length=20, default=0)
    result = models.TextField('返回结果', default='')
    create_time = models.DateTimeField('创建时间', auto_now=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


class ui_suit(models.Model):
    type_choice = ((1, '输入框操作'), (2, '浏览器操作'), (3, '切换页面/窗口'), (4, '其它'))
    action_type = models.IntegerField('操作类型', choices=type_choice, default=0)
    action_choice = ((1, '输入框输入'), (2, '点击输入框'), (3, '清空输入框'), (4, '上传文件'), (5, '打开页面'),
                     (6, '浏览器窗口最大化'), (7, '浏览器返回上一页'), (8, '浏览器前进一页'), (9, '刷新页面'), (10, '关闭当前窗口'),
                     (11, '验证当前URL和值一致'), (12, '截屏'), (13, '等待时间（单位：s）'), (14, '切换iframe'),
                     (15, '切换到alert对话框'), (16, 'alert对话框的确定按钮'), (17, '点击alert对话框的取消按钮'))
    actions = models.IntegerField('操作', choices=action_choice)
    location_fun_choice = ((1, 'id'), (2, 'name'), (3, 'class_name'), (4, 'xpath'), (5, 'css_selector'))
    location_fun = models.IntegerField('定位元素方法', choices=location_fun_choice, default='')
    location = models.CharField('定位/目标', max_length=500, default='')
    value = models.CharField('值', max_length=500, default='')
    ui_id = models.ForeignKey('UiAuto.ui_auto', on_delete=models.CASCADE, to_field="id")
