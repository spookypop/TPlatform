import datetime
import time
from .models import ui_auto, ui_suit
from rest_framework.response import Response
from rest_framework import status
from TPlatform.RunScript import InputSendKeys, InputClick, InputClear, ChromeBrowser, SwitchWindow, OtherAction
from selenium import webdriver


def auto_fun(ui_id):
    suits = ui_suit.objects.filter(ui_id_id=ui_id).order_by('id')
    try:
        # 用windows执行
        # chrome_driver = 'D:\qa\XmindCase\chromedriver.exe'
        # driver = webdriver.Chrome(executable_path=chrome_driver)
        # 用mac执行
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 静默模式启动
        driver = webdriver.Chrome(executable_path='/Users/yehl/Documents/Chromedriver/chromedriver',
                                  chrome_options=option)
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
