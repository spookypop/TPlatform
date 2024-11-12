from django.core.management import BaseCommand
import schedule
import time
from UiAuto.ui_auto_fun import auto_fun


def ci_test():
    print('快点出现。。。。')
    suit_id = 1
    auto_fun(suit_id)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 每隔3秒执行一次
        schedule.every(20).seconds.do(ci_test)
        # schedule.every().day.at('12:42').do(ci_test) # 每天指定时间运行
        schedule.run_pending()
        while True:
            schedule.run_pending()  # 运行所有可以运行的任务
            time.sleep(1)
