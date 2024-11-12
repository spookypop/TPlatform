from django.urls import path
from UiAuto import views

urlpatterns = [
    path(r'createui', views.CreateUi.as_view()),  # 创建自动化测试脚本名称
    path(r'uilist', views.UiList.as_view()),  # 获取自动化测试数据
    path(r'stepdetails', views.StepDetails.as_view()),  # 单个脚本详情
    path(r'run', views.RunScript.as_view()),  # 执行自动化脚本
    path(r'createstep', views.CreateStep.as_view()),  # 创建自动化脚本
    path(r'editstep', views.EditStep.as_view()),  # 编辑脚本
    path(r'stepslist', views.StepsList.as_view()),  # 脚本列表
    path(r'delete_step', views.DeleteStep.as_view()),  # 删除单个脚本
    path(r'delete_ui_suit', views.DeleteUiSuit.as_view()),  # 删除用例集
]
