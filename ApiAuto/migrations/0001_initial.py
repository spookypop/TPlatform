# Generated by Django 4.0.3 on 2022-04-15 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SprintList', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='apiauto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_module', models.CharField(max_length=500, verbose_name='模块名称')),
                ('scene', models.CharField(max_length=500, verbose_name='场景描述')),
                ('api_name', models.CharField(max_length=500, verbose_name='接口地址/名称/关键字')),
                ('assertion_rule', models.CharField(choices=[(0, '响应结果包含'), (1, '请求状态码是')], default=0, max_length=20, verbose_name='校验规则')),
                ('assertion', models.CharField(default='', max_length=500, verbose_name='校验点')),
                ('state', models.CharField(choices=[(0, '未执行'), (1, '通过'), (2, '失败'), (3, '无数据')], default=0, max_length=20, verbose_name='状态')),
                ('result_desc', models.CharField(default='', max_length=500, verbose_name='结果详情')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SprintList.sprints', to_field='sprint_name')),
            ],
        ),
    ]