import os
import sys
import time
import math
from time import sleep
from sys import argv
import random
from pdlearn import version
from pdlearn import user
from pdlearn import dingding
from pdlearn import mydriver
from pdlearn import score
from pdlearn import threads
from pdlearn import get_links
from pdlearn.mydriver import Mydriver


def user_flag(dd_status, uname):
    if False and dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        # if (input("是否保存钉钉帐户密码，保存后可后免登陆学习(Y/N) ")) not in ["y", "Y"]:
        if True:
            driver_login = mydriver.Mydriver(nohead=False)
            cookies = driver_login.login()
            driver_login.quit()
        else:
            cookies = dingding.dd_login_status(uname)
    a_log = user.get_a_log(uname)
    v_log = user.get_v_log(uname)
    d_log = user.get_d_log(uname)

    return cookies, a_log, v_log, d_log


def get_argv():
    nohead = True
    lock = False
    stime = False
    if len(argv) > 2:
        if argv[2] == "hidden":
            nohead = True
        elif argv[2] == "show":
            nohead = False
    if len(argv) > 3:
        if argv[3] == "single":
            lock = True
        elif argv[3] == "multithread":
            lock = False
    if len(argv) > 4:
        if argv[4].isdigit():
            stime = argv[4]
    return nohead, lock, stime


def check_delay():
    delay_time = random.randint(2, 5)
    print('等待 ', delay_time, ' 秒')
    time.sleep(delay_time)


if __name__ == '__main__':
    #  0 读取版本信息
    start_time = time.time()

    print("=" * 60,'''
    科技强国官方网站：https://techxuexi.js.org
    Github地址：https://github.com/TechXueXi
使用本项目，必须接受以下内容，否则请立即退出：
    - TechXueXi 仅额外提供给“爱党爱国”且“工作学业繁重”的人
    - 项目开源协议 LGPL-3.0
    - 不得利用本项目盈利
另外，我们建议你参与一个维护劳动法的项目：
https://996.icu/ 或 https://github.com/996icu/996.ICU/blob/master/README_CN.md
TechXueXi 现支持以下模式（答题时请值守电脑旁处理少部分不正常的题目）：
    1 文章+视频
    2 文章+视频+每日答题
      （可以根据当日已得做题积分，决定是否做题）
    3 文章+视频+每日答题+每周答题+专项答题
      （可以根据当日已得做题积分，及是否有可得分套题，决定是否做题）
''',"=" * 60)
    TechXueXi_mode = input("请选择模式（输入对应数字）并回车： ")
    
    info_shread = threads.MyThread("获取更新信息...", version.up_info)
    info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    dd_status, uname = user.get_user()
    cookies, a_log, v_log, d_log = user_flag(dd_status, uname)
    total, scores = show_score(cookies)
    nohead, lock, stime = get_argv()
    
    article_thread = threads.MyThread("文章学习", article, cookies, a_log, scores, lock=lock)
    video_thread = threads.MyThread("视频学习", video, cookies, v_log, scores, lock=lock)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()
    
    if TechXueXi_mode in ["2", "3"]:
        print('开始每日答题……')
        daily(cookies, d_log, scores)
    if TechXueXi_mode in ["3"]:
        print('开始每周答题……')
        weekly(cookies, d_log, scores)
        print('开始专项答题……')
        zhuanxiang(cookies, d_log, scores)
    
    seconds_used = int(time.time() - start_time)
    print("总计用时 " + str(math.floor(seconds_used / 60)) + " 分 " + str(seconds_used % 60) + " 秒")
    user.shutdown(stime)
