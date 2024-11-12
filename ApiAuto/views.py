from rest_framework.views import APIView
from rest_framework.response import Response
from .models import apiauto
from SprintList.models import sprints
from rest_framework import status
from .serializer import ApiSerializer
from TPlatform.TokenAuth import TokenAuth
import io
import re
import os


# Create your views here.
# 创建接口用例
class CreateApi(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        api_module = request.data.get('api_module')
        scene = request.data.get('scene')
        api_name = request.data.get('api_name')
        assertion_rule = request.data.get('assertion_rule')
        assertion = request.data.get('assertion')
        if sprint_name and api_module and scene and api_name and assertion_rule and assertion:
            sprint_result = sprints.objects.get(sprint_name=sprint_name)
            try:
                apiauto.objects.create(name_id=sprint_result.sprint_name, api_module=api_module, api_name=api_name,
                                       scene=scene,
                                       assertion_rule=assertion_rule, assertion=assertion)
                result = {"status": "200", "data": {'msg': 'OK'}}
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                result = {"status": "500", "data": e}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '参数不能为空'}}
            return Response(result, status=status.HTTP_200_OK)


# 获取接口列表
class ApiList(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        if sprint_name:
            if sprints.objects.filter(sprint_name=sprint_name):
                sprint_result = sprints.objects.get(sprint_name=sprint_name)
                api_list = apiauto.objects.filter(name_id=sprint_result.sprint_name)
                serialize = ApiSerializer(api_list, many=True)
                result = {"status": "200", "data": serialize.data}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": "500", "data": {'msg': '迭代不存在'}}
                return Response(result, status=status.HTTP_200_OK)
        else:
            # api_list = apiauto.objects.all()
            # serialize = ApiSerializer(api_list, many=True)
            result = {"status": "200", "data": []}
            return Response(result, status=status.HTTP_200_OK)


# 运行接口用例
class ExecuteApi(APIView):
    def post(self, request):
        id = request.data.get('id')
        api_name = request.data.get('api_name')
        # assertion_rule = request.data.get('assertion_rule')
        assertion = request.data.get('assertion')
        # 日志地址
        path = r'D:\\python\\Scripts\\XmindCase\\logs\\all-2021-07-28.log'
        if api_name and assertion:
            num = self.load_log(path, api_name, assertion)  # num用例成功数，最近匹配一条则为成功
            print(num)
            if num > 0:
                apiauto.objects.filter(id=id).update(state=1, result_desc='通过')
                result = {"status": "200", "data": "用例通过"}
                return Response(result, status=status.HTTP_200_OK)
            else:
                apiauto.objects.filter(id=id).update(state=2, result_desc='预期结果无匹配数据')
                result = {"status": "101", "data": "用例不通过"}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": "参数不能为空"}
            return Response(result, status=status.HTTP_200_OK)

    # 逆序按行读取文件
    def readlines_reverse(self, path):
        with io.open(path, mode="r", encoding='unicode_escape', errors='ignore')  as qfile:
            qfile.seek(0, os.SEEK_END)
            # tell() 方法返回文件的当前位置，即文件指针当前位置。
            position = qfile.tell()
            line = ''
            while position >= 0:
                qfile.seek(position)
                next_char = qfile.read(1)
                if next_char == "\n":
                    yield line[::-1]
                    line = ''
                else:
                    line += next_char
                position -= 1
            yield line[::-1]

    def load_log(self, path, api_name, assertion):
        count = 0
        for line in self.readlines_reverse(path):
            line = line.strip()
            print(line)
            result = self.parse_rule1(line, api_name, assertion)
            if result == "matching":
                count = count + 1
                break
            else:
                print("该行匹配失败")
        return count

    # 解析日志，规则1：请求状态码是XXX
    def parse_rule1(self, line, api_name, assertion):
        pattern = '(\w*) (\S*)' + api_name + ' (.*) ' + assertion
        print(api_name)
        obj = re.compile(pattern)
        # result = re.search(obj,line)
        result = obj.findall(line)
        if not result:
            return "fail"
        else:
            return "matching"
