from django.urls import path
from SprintList import views

urlpatterns = [
    path(r'createsprint', views.Sprint.as_view()),  # 创建迭代
    path(r'sprintlist', views.SprintList.as_view()),  # 迭代列表
    path(r'caselist/<str:sprint_name>', views.CaseList.as_view()),  # 查询某个迭代的测试用例
    path(r'caseimport', views.CasesImport.as_view()),  # xmind用例导入
    path(r'update_result', views.ExecuteCase.as_view()),  # 用例执行结果更改
    path(r'sprintexist', views.SprintExist.as_view()),  # 查询迭代名称是否存在
    path(r'updatesprint', views.UpdateSprint.as_view()),  # 更新迭代状态
    path(r'delete_case', views.DeleteCase.as_view()),  # 删除单条测试用例
    path(r'create_case', views.CreateCase.as_view()),  # 新增单条测试用例
    path(r'count_case', views.CountCase.as_view()),  # 功能测试用例执行进度统计
]