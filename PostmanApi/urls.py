"""PostmanApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PostmanApi import views

urlpatterns = [
    path(r'upload_file', views.FileUpload.as_view()),  # 上传文件
    path(r'file_list', views.FileList.as_view()),  # 文件列表
    path(r'delete_file', views.DeleteFile.as_view()),  # 删除文件
    path(r'file_content', views.FileContent.as_view()),  # 文件内容
    path(r'run_collections', views.RunCollections.as_view()),  # 运行集合--批量运行
    path(r'run_collection', views.RunACollection.as_view()),  # 运行单个集合
]
