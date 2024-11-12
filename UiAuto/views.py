import datetime
import os
import time
from pathlib import Path
from rest_framework.views import APIView
from .models import ui_auto, ui_suit
from rest_framework.response import Response
from rest_framework import status
from .serialize import Uiserializer, Suitserializer
from TPlatform.RunScript import InputSendKeys, InputClick, InputClear, ChromeBrowser, SwitchWindow, OtherAction
from selenium import webdriver
from TPlatform.TokenAuth import TokenAuth
from TPlatform.find_action_type import find_type


# 新建自动化测试脚本名称
class CreateUi(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        ui_name = request.data.get('ui_name')
        if ui_name:
            try:
                ui_auto.objects.create(ui_name=ui_name)
                result = {"status": "200", "data": {'msg': 'OK'}}
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                result = {"status": "500", "data": e}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": {'msg': '参数不能为空'}}
            return Response(result, status=status.HTTP_200_OK)


# 获取所有自动化脚本名称
class UiList(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        try:
            ui_list = ui_auto.objects.all()
            serialize = Uiserializer(ui_list, many=True)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as e:
            result = {"status": "500", "data": e}
            return Response(result, status=status.HTTP_200_OK)


# 创建自动化脚本
class CreateStep(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        ui_id = request.data.get('ui_id')
        actions = request.data.get('actions')
        location_fun = request.data.get('location_fun')
        location = request.data.get('location')
        value = request.data.get('value')
        action_type = find_type(actions)
        if actions:
            if location == 'undefined':
                location = ''
            if value == 'undefined':
                value = ''
            if location_fun == 'undefined':
                location_fun = 0
            ui_suit.objects.create(action_type=action_type, actions=actions, location_fun=location_fun,
                                   location=location, value=value, ui_id_id=ui_id)

            result = {"status": "200", "data": "ok"}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": "参数不能为空"}
            return Response(result, status=status.HTTP_200_OK)


# 单个场景的脚本列表集
class StepsList(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        ui_id = request.data.get('ui_id')
        if ui_id:
            step_list = ui_suit.objects.filter(ui_id_id=ui_id).order_by('id')
            serialize = Suitserializer(step_list, many=True)
            result = {"status": "200", "data": serialize.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": "参数不能为空"}
            return Response(result, status=status.HTTP_200_OK)


# 查询单个脚本详情
class StepDetails(APIView):

    def post(self, request):
        id = request.data.get('id')
        if id:
            step = ui_suit.objects.get(id=id)
            serialize = Suitserializer(step)
            result = {"status": "200", "data": serialize.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": "参数不能为空"}
            return Response(result, status=status.HTTP_200_OK)


# 编辑自动化脚本
class EditStep(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        id = request.data.get('id')
        actions = request.data.get('actions')
        location_fun = request.data.get('location_fun')
        location = request.data.get('location')
        value = request.data.get('value')
        action_type = find_type(actions)
        # 非必填项，前端传undefined时转为空值
        if actions:
            if location == 'undefined':
                location = ''
            if value == 'undefined':
                value = ''
            if location_fun == 'undefined':
                location_fun = 0
        try:
            ui_suit.objects.filter(id=id).update(action_type=action_type, actions=actions,
                                                 location_fun=location_fun,
                                                 location=location, value=value)
            result = {"status": "200", "data": "ok"}
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {"status": "500", "data": e}
            return Response(result, status=status.HTTP_200_OK)


# 删除单个脚本
class DeleteStep(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        id = request.data.get('id')
        try:
            ui_suit.objects.get(id=id).delete()
            result = {"status": "200", "data": "ok"}
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {"status": "500", "data": e}
            return Response(result, status=status.HTTP_200_OK)


# 执行自动化测试脚本
class RunScript(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        ui_id = request.data.get('ui_id')
        suits = ui_suit.objects.filter(ui_id_id=ui_id).order_by('id')
        try:
            # 用windows执行
            # chrome_driver = 'D:\qa\XmindCase\chromedriver.exe'
            # driver = webdriver.Chrome(executable_path=chrome_driver)
            # 用mac执行
            option = webdriver.ChromeOptions()
            # option.add_argument('headless')  # 静默模式启动
            base_dir = Path(__file__).resolve().parent.parent
            chrome_path = os.path.join(base_dir, 'chromedriver')
            driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)
            # driver.set_window_size(800, 800)
            time.sleep(2)
            for suit in suits:
                # 输入框操作
                # 输入框输入值
                if suit.action_type == 1:
                    if suit.actions == 1:
                        if suit.location_fun and suit.location and suit.value:
                            if suit.location_fun == 1:
                                InputSendKeys.id_key(driver, suit.location, suit.value)
                            elif suit.location_fun == 2:
                                InputSendKeys.name_key(driver, suit.location, suit.value)
                            elif suit.location_fun == 3:
                                InputSendKeys.class_key(driver, suit.location, suit.value)
                            elif suit.location_fun == 4:
                                InputSendKeys.xpath_key(driver, suit.location, suit.value)
                            elif suit.location_fun == 5:
                                InputSendKeys.css_key(driver, suit.location)
                            else:
                                result = {"status": "500", "data": {'case_id': suit.id, 'msg': "用例步骤不存在"}}
                                ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                        update_time=datetime.datetime.now())
                                return Response(result, status=status.HTTP_200_OK)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "输入框输入，定位元素方法、定位/目标、值不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                    elif suit.actions == 2:
                        # 输入框点击操作
                        if suit.location_fun and suit.location:
                            if suit.location_fun == 1:
                                InputClick.id_click(driver, suit.location)
                            elif suit.location_fun == 2:
                                InputClick.name_click(driver, suit.location)
                            elif suit.location_fun == 3:
                                InputClick.class_click(driver, suit.location)
                            elif suit.location_fun == 4:
                                InputClick.xpath_click(driver, suit.location)
                            elif suit.location_fun == 5:
                                InputClick.css_click(driver, suit.location)
                            else:
                                result = {"status": "500", "data": {'case_id': suit.id, 'msg': "用例步骤不存在"}}
                                ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                        update_time=datetime.datetime.now())
                                return Response(result, status=status.HTTP_200_OK)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "输入框点击，定位元素方法、定位/目标不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                            # 输入框清空
                    elif suit.actions == 3:
                        if suit.location_fun and suit.location:
                            if suit.location_fun == 1:
                                InputClear.id_clear(driver, suit.location)
                            elif suit.location_fun == 2:
                                InputClear.name_clear(driver, suit.location)
                            elif suit.location_fun == 3:
                                InputClear.class_clear(driver, suit.location)
                            elif suit.location_fun == 4:
                                InputClear.xpath_clear(driver, suit.location)
                            elif suit.location_fun == 5:
                                InputClear.class_clear(driver, suit.location)
                            else:
                                result = {"status": "500", "data": {'case_id': suit.id, 'msg': "用例步骤不存在"}}
                                ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                        update_time=datetime.datetime.now())
                                return Response(result, status=status.HTTP_200_OK)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "输入框清空，定位元素方法、定位/目标不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)

                    else:
                        result = {"status": "500", "data": {'case_id': suit.id, 'msg': "操作类型错误"}}
                        ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                update_time=datetime.datetime.now())
                        return Response(result, status=status.HTTP_200_OK)
                # 浏览器操作
                elif suit.action_type == 2:
                    if suit.actions == 5:
                        if suit.value:
                            ChromeBrowser.open_url(driver, suit.value)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "值不能为空", }}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                    elif suit.actions == 6:
                        ChromeBrowser.max_window(driver)
                    elif suit.actions == 7:
                        ChromeBrowser.browser_back(driver)
                    elif suit.actions == 8:
                        ChromeBrowser.browser_forward(driver)
                    elif suit.actions == 9:
                        ChromeBrowser.refresh(driver)
                    elif suit.actions == 10:
                        ChromeBrowser.browser_close(driver)
                    else:
                        result = {"status": "500", "data": {'case_id': suit.id, 'msg': "用例步骤不存在"}}
                        ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                update_time=datetime.datetime.now())
                        return Response(result, status=status.HTTP_200_OK)
                # 切换窗口
                elif suit.action_type == 3:
                    if suit.actions == 14:
                        if suit.value:
                            SwitchWindow.switch_frame(driver, suit.value)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "值不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                    elif suit.actions == 15:
                        SwitchWindow.switch_alert(driver)
                    elif suit.actions == 16:
                        SwitchWindow.alert_accept(driver)
                    elif suit.actions == 17:
                        SwitchWindow.alert_dismiss(driver)
                    else:
                        result = {"status": "500", "data": {'case_id': suit.id, 'msg': "用例步骤不存在"}}
                        ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                update_time=datetime.datetime.now())
                        return Response(result, status=status.HTTP_200_OK)
                # 其它操作
                elif suit.action_type == 4:
                    if suit.actions == 13:
                        if suit.value:
                            OtherAction.wait_time(driver, suit.value)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "值不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                    elif suit.actions == 11:
                        if suit.value:
                            OtherAction.assertion_url(driver, suit.value)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "值不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                    elif suit.actions == 12:
                        if suit.value:
                            OtherAction.get_screenshot(driver, suit.value)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "值不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                    elif suit.actions == 4:
                        if suit.location:
                            OtherAction.upload_file(driver, suit.location)
                        else:
                            result = {"status": "500", "data": {'case_id': suit.id, 'msg': "值不能为空"}}
                            ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                    update_time=datetime.datetime.now())
                            return Response(result, status=status.HTTP_200_OK)
                    else:
                        result = {"status": "500", "data": {'case_id': suit.id, 'msg': "用例步骤不存在"}}
                        ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                                update_time=datetime.datetime.now())
                        return Response(result, status=status.HTTP_200_OK)

                else:
                    result = {"status": "500", "data": {'case_id': suit.id, 'msg': "用例步骤不存在"}}
                    ui_auto.objects.filter(id=ui_id).update(state=2, result=result,
                                                            update_time=datetime.datetime.now())
                    return Response(result, status=status.HTTP_200_OK)
            driver.quit()
            ui_auto.objects.filter(id=ui_id).update(state=1, result="成功", update_time=datetime.datetime.now())
            result = {"status": "200", "data": "ok"}
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            ui_auto.objects.filter(id=ui_id).update(state=2, result=e, update_time=datetime.datetime.now())
            result = {"status": "500", "data": "失败"}
            return Response(result, status=status.HTTP_200_OK)


# 删除场景的脚本集
class DeleteUiSuit(APIView):
    authentication_classes = [TokenAuth]

    def post(self, request):
        id = request.data.get('id')
        if id:
            try:
                ui_auto.objects.get(id=id).delete()
                result = {"status": "200", "data": "ok"}
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                result = {"status": "500", "data": e}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {"status": "500", "data": "参数不能为空"}
            return Response(result, status=status.HTTP_200_OK)
