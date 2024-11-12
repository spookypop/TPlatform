from rest_framework.views import APIView
from rest_framework.response import Response
from SprintList.models import sprints, cases
from rest_framework import status
from SprintList.serializer import SprintSerializer, CaseSerializer
from xmindparser import xmind_to_dict
from TPlatform.TokenAuth import TokenAuth


# sprint
# 创建迭代:输入迭代名称创建
class Sprint(APIView):
    # 登录权限验证
    authentication_classes = [TokenAuth]

    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        if sprint_name:
            # 查询迭代名称是否已存在
            if sprints.objects.filter(sprint_name=sprint_name).count() < 1:
                # 新增迭代，数据库新增一条数据
                sprints.objects.create(sprint_name=sprint_name)
                result = {"status": "200", "data": {'msg': 'OK'}}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": "500", "data": {'msg': '迭代名称已存在'}}
                return Response(result)
        else:
            result = {"status": "500", "data": {'msg': '迭代名称不能为空'}}
            return Response(result)

    # 删除迭代
    def delete(self, request):
        sprint_name = request.data.get('sprint_name')
        username = request.data.get('username')
        sprints.objects.get(sprint_name=sprint_name).delete()
        if sprints.objects.filter(sprint_name=sprint_name).count() < 1:
            result = {"status": "200", "data": {'msg': 'OK'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '删除失败'}}
            return Response(result, status=status.HTTP_200_OK)


# 查询所有迭代数据库
class SprintList(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        # username = request.data.get('username')
        sprint_list = sprints.objects.all()
        serialize = SprintSerializer(sprint_list, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)


# 更新迭代状态
class UpdateSprint(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        state = request.data.get('state')
        if sprints.objects.filter(sprint_name=sprint_name).count() == 1:
            sprints.objects.filter(sprint_name=sprint_name).update(state=state)
            result = {"status": "200", "data": {'msg': 'OK'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '更新失败'}}
            return Response(result, status=status.HTTP_200_OK)


# 查询迭代名称是否重复
class SprintExist(APIView):
    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        if sprints.objects.filter(sprint_name=sprint_name).count() < 1:
            result = {"status": "200", "data": {'msg': 'OK'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '迭代名称已存在'}}
            return Response(result)


# 获取某个迭代的测试用例
class CaseList(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request, sprint_name):
        if sprint_name:
            result = sprints.objects.get(sprint_name=sprint_name)
            sprint_cases = cases.objects.filter(sprint_name_id=result.id).order_by('result', 'id')
            serialize = CaseSerializer(sprint_cases, many=True)
            return Response(serialize.data)
        else:
            result = {"status": "500", "data": {'msg': '迭代名称不能为空'}}
            return Response(result, status=status.HTTP_200_OK)


# case
# xind测试用例导入
class CasesImport(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        file_path = request.data.get('file_path')  # 可以是文件路径，实际读的是文件对象
        result = sprints.objects.get(sprint_name=sprint_name)
        if file_path:
            content = xmind_to_dict(file_path)  # Xmind文件解析为字典格式
            xmind_cases = content[0]['topic']['topics']  # 用例集
            # print(xmind_cases[0]['topics'][0]['topics'][0]['title']) 读取第一条测试用例描述
            app_len = len(xmind_cases)  # 系统/应用/页面个数，xmind用例二级分类的个数
            for i in range(0, app_len):
                app_name = xmind_cases[i]['title']  # 系统/应用/页面名称
                module_len = len(xmind_cases[i]['topics'])  # 各模块用例数
                module_case = xmind_cases[i]['topics']  # 各模块用例集
                i += 1
                for j in range(0, module_len):
                    module_name = module_case[j]['title']  # 模块名称
                    cases_suits = module_case[j]['topics']
                    case_len = len(cases_suits)  # 每个模块的用例数
                    j += 1
                    for k in range(0, case_len):
                        case_description = cases_suits[k]['title']
                        cases.objects.create(app_name=app_name, module_name=module_name,
                                             case_description=case_description, sprint_name_id=result.id)
            result = {"status": "200", "data": {'msg': 'OK'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '导入失败'}}
            return Response(result, status=status.HTTP_200_OK)


# 手动新增测试用例
class CreateCase(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        app_name = request.data.get('app_name')
        module_name = request.data.get('module_name')
        case_description = request.data.get('case_description')
        case_data = request.data.get('case_data')
        if case_data == 'undefined':
            case_data = ''
        if sprint_name and app_name and module_name and case_description:
            if sprints.objects.filter(sprint_name=sprint_name):
                result = sprints.objects.get(sprint_name=sprint_name)
                cases.objects.create(app_name=app_name, module_name=module_name, case_data=case_data,
                                     case_description=case_description,
                                     sprint_name_id=result.id)
                result = {"status": "200", "data": {'msg': 'OK'}}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": "500", "data": {'msg': '迭代不存在'}}
                return Response(result, status=status.HTTP_200_OK)
        result = {"status": "500", "data": {'msg': '参数不能为空'}}
        return Response(result, status=status.HTTP_200_OK)


# 用例执行结果
class ExecuteCase(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        case_id = request.data.get('case_id')
        result = request.data.get('result')
        if case_id and result:
            cases.objects.filter(id=case_id).update(result=result)
            result = {"status": "200", "data": {'msg': 'ok'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '缺少参数'}}
            return Response(result, status=status.HTTP_200_OK)


# 删除测试用例
class DeleteCase(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        case_id = request.data.get('case_id')
        if case_id:
            cases.objects.filter(id=case_id).delete()
            result = {"status": "200", "data": {'msg': 'OK'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '缺少参数'}}
            return Response(result, status=status.HTTP_200_OK)


# 功能测试用例执行进度统计
class CountCase(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        sprint_name = request.data.get('sprint_name')
        caselist = sprints.objects.get(sprint_name=sprint_name)  # 获取迭代ID
        if caselist:
            total = cases.objects.filter(sprint_name_id=caselist.id).count()
            if total > 0:
                pass_count = cases.objects.filter(sprint_name_id=caselist.id, result='3').count()
                failure_count = cases.objects.filter(sprint_name_id=caselist.id, result='1').count()
                # 挂起的测试用例（本次迭代暂时不做的功能）
                suspend_count = cases.objects.filter(sprint_name_id=caselist.id, result='2').count()
                progress = (pass_count + suspend_count) / total * 100
                progress = ('%.2f' % progress)
                fail_case = failure_count / total * 100
                fail_case = ('%.2f' % fail_case)
                print(fail_case)
                result = {"status": "200", "data": {'progress': progress, 'fail_case': fail_case}}
                return Response(result, status=status.HTTP_200_OK)
            else:
                progress = 0
                fail_case = 0
                result = {"status": "200", "data": {'progress': progress, 'fail_case': fail_case}}
                return Response(result, status=status.HTTP_200_OK)

        else:
            result = {"status": "500", "data": {'msg': '迭代不存在'}}
            return Response(result, status=status.HTTP_200_OK)
