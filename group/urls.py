from django.urls import path
from group import views

urlpatterns = [
    path(r'register', views.Register.as_view()),  # django内置的用户管理
    path(r'login', views.Login.as_view()),  # 用户登录
    path(r'logout', views.Logout.as_view()),  # 退出登录
    path(r'loginuser', views.LoginUser.as_view()),
    path(r'userList', views.UserList.as_view()),  # 用户列表
]
