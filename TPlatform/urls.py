"""XmindCase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from group import urls as group_urls
from ApiAuto import urls as api_urls
from UiAuto import urls as ui_urls
from SprintList import urls as case_url
from PostmanApi import urls as postman_urls

urlpatterns = [
    path(r'group/', include(group_urls), name='group'),  # 用户应用的urls
    path(r'api/', include(api_urls), name='ApiAuto'),
    path(r'ui/', include(ui_urls), name='UiAuto'),
    path(r'case/', include(case_url), name='SprintList'),
    path(r'postman/', include(postman_urls), name='PostmanApi')

]

