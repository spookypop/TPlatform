import os
from rest_framework.views import APIView
from TPlatform import settings
from PostmanApi.models import CollectionList
from rest_framework.response import Response
from rest_framework import status
from .serializser import PostmanSerializer
from TPlatform.TokenAuth import TokenAuth


# 文件上传
class FileUpload(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        file_type = request.data.get('file_type')
        collection_name = request.data.get('collection_name')
        file = request.FILES.get('file', None)
        print(file_type, collection_name)
        if file_type == '2':
            if CollectionList.objects.filter(file_type='2'):
                result = {"status": "500", "data": {'msg': '全局变量文件已存在，不能重复上传'}}
                return Response(result, status=status.HTTP_200_OK)
        if file is not None:
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            file_name = file.name
            if not os.path.exists(file_path):
                try:
                    with open(file_path, 'wb') as f:
                        # 分块写入
                        for chunk in file.chunks():
                            f.write(chunk)
                        f.close()
                    CollectionList.objects.create(collection_name=collection_name, file_name=file_name,
                                                  file_type=file_type, file_path=file_path)
                    result = {"status": "200", "data": {'msg': '上传成功'}}
                    return Response(result, status=status.HTTP_200_OK)
                except Exception as e:
                    result = {"status": "500", "data": e}
                    return Response(result, status=status.HTTP_200_OK)
            else:
                result = {"status": "500", "data": {'msg': '文件名重复'}}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '文件不能为空'}}
            return Response(result, status=status.HTTP_200_OK)


# file list
class FileList(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        file_type = request.data.get('file_type')
        if file_type is None:
            file_list = CollectionList.objects.all()
            serializer = PostmanSerializer(file_list, many=True)
            result = {"status": "200", "data": serializer.data}
            return Response(result, status=status.HTTP_200_OK)

        else:
            file_list = CollectionList.objects.filter(file_type=file_type)
            serializer = PostmanSerializer(file_list, many=True)
            result = {"status": "200", "data": serializer.data}
            return Response(result, status=status.HTTP_200_OK)


# 文件删除
class DeleteFile(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        file_id = request.data.get('id')
        file_find = CollectionList.objects.get(id=file_id)
        file_path = file_find.file_path
        if os.path.exists(file_path):
            os.remove(file_path)
            CollectionList.objects.filter(id=file_id).delete()
            result = {"status": "200", "data": {'msg': '删除成功'}}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '文件不存在'}}
            return Response(result, status=status.HTTP_200_OK)


# 查看文件内容
class FileContent(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        file_id = request.data.get('id')
        file_find = CollectionList.objects.get(id=file_id)
        file_path = file_find.file_path
        with open(file_path, 'r') as file:
            list1 = file.readlines()
            for i in range(0, len(list1)):
                list1[i] = list1[i].strip('\n')
                list1[i] = list1[i].strip('\t')
            file.close()
        return Response(list1, status=status.HTTP_200_OK)


# 运行集合--批量运行
class RunCollections(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        collection_id = request.data.get('collection_id')
        environment_id = request.data.get('environment_id')
        data_id = request.data.get('data_id')
        iteration = request.data.get('iteration')
        delay = request.data.get('delay')
        global_id = CollectionList.objects.filter(file_type='2')  # 查找是否有全局变量文件
        data_file = CollectionList.objects.get(id=data_id)  # 获取数据文件
        environment_file = CollectionList.objects.get(id=environment_id)  # 获取环境变量文件
        global_file = CollectionList.objects.get(file_type='2')
        if collection_id is not None:
            collection_file = CollectionList.objects.get(id=collection_id)  # 获取集合文件
            if (environment_id is not None) and (global_id is not None):
                report = os.popen(f'newman run {collection_file.file_path} --environment '
                                  f'{environment_file.file_path} --globals {global_file.file_path} '
                                  f'--iteration-count {iteration} --iteration-data {data_file.file_path} --delay'
                                  f'-request {int(delay)}')
            elif environment_id is not None:
                report = os.popen(f'newman run {collection_file.file_path} --environment '
                                  f'{environment_file.file_path} '
                                  f'--iteration-count {iteration} --iteration-data {data_file.file_path} --delay'
                                  f'-request {int(delay)}')
            elif global_id is not None:
                report = os.popen(f'newman run {collection_file.file_path}  '
                                  f' --globals {global_file.file_path} '
                                  f'--iteration-count {iteration} --iteration-data {data_file.file_path} --delay'
                                  f'-request {int(delay)}')
            else:
                report = os.popen(f'newman run {collection_file.file_path}  '
                                  f'--iteration-count {iteration} --iteration-data {data_file.file_path} --delay'
                                  f'-request {int(delay)}')
            result = []
            for line in report.readlines():
                line = line.strip('\n')
                result.append(line)
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '参数不能为空'}}
            return Response(result, status=status.HTTP_200_OK)


# 运行集合
class RunACollection(APIView):
    # authentication_classes = [TokenAuth]

    def post(self, request):
        collection_id = request.data.get('collection_id')
        environment_id = request.data.get('environment_id')
        delay = request.data.get('delay')
        print(collection_id, environment_id, delay)
        global_id = CollectionList.objects.filter(file_type='2')  # 查找是否有全局变量文件
        environment_file = CollectionList.objects.get(id=environment_id)  # 获取环境变量文件
        global_file = CollectionList.objects.get(file_type='2')
        if environment_id == 'undefined':
            environment_id = ''
        if collection_id is not None:
            collection_file = CollectionList.objects.get(id=collection_id)  # 获取集合文件
            if (environment_id is not None) and (global_id is not None):
                report = os.popen(f'newman run {collection_file.file_path} --environment '
                                  f'{environment_file.file_path} --globals {global_file.file_path} '
                                  f' --delay-request {int(delay)} ')
            elif environment_id is not None:
                report = os.popen(f'newman run {collection_file.file_path} --environment '
                                  f'{environment_file.file_path} '
                                  f'--delay-request {int(delay)}'
                                  )
            elif global_id is not None:
                report = os.popen(f'newman run {collection_file.file_path}  '
                                  f' --globals {global_file.file_path} '
                                  f' --delay-request {int(delay)} --reporter-cli-no-summary')
            else:
                report = os.popen(f'newman run {collection_file.file_path}  '
                                  f' --delay-request {int(delay)}')
            result = []
            for line in report.readlines():
                line = line.strip('\n')
                result.append(line)
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '参数不能为空'}}
            return Response(result, status=status.HTTP_200_OK)
