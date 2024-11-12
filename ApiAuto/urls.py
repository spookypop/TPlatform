from django.urls import path
from ApiAuto import views

urlpatterns = [
    path(r'createapi', views.CreateApi.as_view()),  # 创建接口
    path(r'apilist', views.ApiList.as_view()),  # 接口列表
    path(r'runapi', views.ExecuteApi.as_view()),  # 运行接口用例
]
