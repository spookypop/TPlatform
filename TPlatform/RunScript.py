import os
import time


# 输入框输入
class InputSendKeys:
    def id_key(driver, location, value):
        driver.find_element_by_id(location).send_keys(value)
        time.sleep(1)

    def name_key(driver, location, value):
        driver.find_element_by_name(location).send_keys(value)
        time.sleep(1)

    def class_key(driver, location, value):
        driver.find_element_by_class_name(location).send_keys(value)
        time.sleep(1)

    def xpath_key(driver, location, value):
        driver.find_element_by_xpath(location).send_keys(value)
        time.sleep(1)

    def css_key(driver, location, value):
        driver.find_element_by_css_selector(location).send_keys(value)
        time.sleep(1)


# 输入框点击
class InputClick:
    def id_click(driver, location):
        driver.find_element_by_id(location).click()
        time.sleep(1)

    def name_click(driver, location):
        driver.find_element_by_name(location).click()
        time.sleep(1)

    def class_click(driver, location):
        driver.find_element_by_class_name(location).click()
        time.sleep(1)

    def xpath_click(driver, location):
        driver.find_element_by_xpath(location).click()
        time.sleep(1)

    def css_click(driver, location):
        driver.find_element_by_css_selector(location).click()
        time.sleep(1)


# 输入框清空
class InputClear:
    def id_clear(driver, location):
        driver.find_element_by_id(location).clear()
        time.sleep(1)

    def name_clear(driver, location):
        driver.find_element_by_name(location).clear()
        time.sleep(1)

    def class_clear(driver, location):
        driver.find_element_by_class_name(location).clear()
        time.sleep(1)

    def xpath_clear(driver, location):
        driver.find_element_by_xpath(location).clear()
        time.sleep(1)

    def css_clear(driver, location):
        driver.find_element_by_css_selector(location).clear()
        time.sleep(1)


#  谷歌浏览器操作
class ChromeBrowser:
    # 打开页面
    def open_url(driver, value):
        driver.get(value)
        time.sleep(1)

    # 关闭浏览器窗口
    def browser_close(driver):
        driver.close()

    # 当前页面刷新
    def refresh(driver):
        driver.refresh()
        time.sleep(1)

    # 浏览器窗口最大化
    def max_window(driver):
        driver.maximize_window()
        time.sleep(1)

    # 浏览器返回上一页
    def browser_back(driver):
        driver.back()
        time.sleep(1)

    # 浏览器前进一页
    def browser_forward(driver):
        driver.forward()
        time.sleep(1)


# 切换窗口
class SwitchWindow:
    # 先支持通过xpth来查找
    def switch_frame(driver, value):
        fm = driver.find_element_by_xpath(value)
        driver.switch_to.frame(fm)
        time.sleep(1)

    # 访问alert对话框
    def switch_alert(driver):
        driver.switch_to.alert()
        time.sleep(1)

    # alert对话框的确定按钮
    def alert_accept(driver):
        driver.switch_to.alert.accept()
        time.sleep(1)

    # 点击alert对话框的取消按钮
    def alert_dismiss(driver):
        driver.switch_to.alert.dismiss()
        time.sleep(1)


# 其他不常用的操作
class OtherAction:
    def wait_time(driver, value):
        time.sleep(value)

    # 验证当前页面url,校验页面跳转是否正确
    def assertion_url(driver, value):
        assert driver.current_url == value, '页面地址验证失败'

    # 截屏
    def get_screenshot(driver, value):
        driver.get_screenshot_as_file(value)  # 截屏保存路径应完整，如输入“c: / ven / test.jpg”
        time.sleep(1)

    def upload_file(driver, location):
        driver.find_element_by_xpath(location).click()
        time.sleep(2)
        os.system(r"D:\qa\XmindCase\uploadfile.exe")
        time.sleep(3)
