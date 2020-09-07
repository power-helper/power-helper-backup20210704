import time
from sys import argv
import random
from pdlearn import version
from pdlearn import user
from pdlearn import dingding
from pdlearn import mydriver
from pdlearn import score
from pdlearn import threads
from pdlearn import get_links


def user_flag(dd_status, uname):
    if False and dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        # if (input("是否保存钉钉帐户密码，保存后可后免登陆学习(Y/N) ")) not in ["y", "Y"]:
        if True:
            driver_login = mydriver.Mydriver(nohead=False)
            cookies = driver_login.login()
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


def show_score(cookies):
    total, each = score.get_score(cookies)
    print("当前学习总积分：" + str(total))
    print("阅读文章:{}/6,观看视频:{}/6,登陆:{}/1,文章时长:{}/6,视频时长:{}/6,每日答题:{}/6,每周答题:{}/5,专项答题:{}/10".format(*each))
    return total, each


def article(cookies, a_log, each):
    if each[0] < 6 or each[3] < 8:
        driver_article = mydriver.Mydriver(nohead=nohead)
        driver_article.get_url("https://www.xuexi.cn/notFound.html")
        driver_article.set_cookies(cookies)
        links = get_links.get_article_links()
        try_count = 0
        readarticle_time = 0
        while True:
            if each[0] < 6 and try_count < 10:
                a_num = 6 - each[0]
                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    readarticle_time = 60+random.randint(5, 15)
                    for j in range(readarticle_time):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                        print("\r文章学习中，文章剩余{}篇,本篇剩余时间{}秒".format(a_log + a_num - i, readarticle_time - j), end="")
                        time.sleep(1)
                    driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = show_score(cookies)
                    if each[0] >= 6:
                        print("检测到文章数量分数已满,退出学习")
                        break
                a_log += a_num
            else:
                with open("./user/{}/a_log".format(uname), "w", encoding="utf8") as fp:
                    fp.write(str(a_log))
                break
        try_count = 0
        while True:
            if each[3] < 6 and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log - 1])
                remaining = (6 - each[3]) * 1 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (60) == 0 and i != remaining:
                        total, each = show_score(cookies)
                        if each[3] >= 6:
                            print("检测到文章时长分数已满,退出学习")
                            break
                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("文章学习完成")
        else:
            print("文章学习出现异常，请检查用户名下a_log文件记录数")
        driver_article.quit()
    else:
        print("文章之前学完了")


def video(cookies, v_log, each):
    if each[1] < 6 or each[4] < 10:
        driver_video = mydriver.Mydriver(nohead=nohead)
        driver_video.get_url("https://www.xuexi.cn/notFound.html")
        driver_video.set_cookies(cookies)
        links = get_links.get_video_links()
        try_count = 0
        watchvideo_time = 0
        while True:
            if each[1] < 6 and try_count < 10:
                v_num = 6 - each[1]
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    watchvideo_time = 60+random.randint(5, 15)
                    for j in range(watchvideo_time):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                        print("\r视频学习中，视频剩余{}个,本次剩余时间{}秒".format(v_log + v_num - i, watchvideo_time - j), end="")
                        time.sleep(1)
                    driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, each = show_score(cookies)
                    if each[1] >= 6:
                        print("检测到视频数量分数已满,退出学习")
                        break
                v_log += v_num
            else:
                with open("./user/{}/v_log".format(uname), "w", encoding="utf8") as fp:
                    fp.write(str(v_log))
                break
        try_count = 0
        while True:
            if each[4] < 6 and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log - 1])
                remaining = (6 - each[4]) * 1 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r视频学习中，视频总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (60) == 0 and i != remaining:
                        total, each = show_score(cookies)
                        if each[4] >= 6:
                            print("检测到视频时长分数已满,退出学习")
                            break
                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("视频学习完成")
        else:
            print("视频学习出现异常，请检查用户名下v_log文件记录数")
        driver_video.quit()
    else:
        print("视频之前学完了")


def daily(cookies, d_log, each):
    if each[5] < 6:
        # driver_daily = mydriver.Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_daily = mydriver.Mydriver(nohead=False)
        driver_daily.get_url("https://www.xuexi.cn/notFound.html")
        driver_daily.set_cookies(cookies)
        try_count = 0
        while True:
            if each[5] < 6 and try_count < 10:
                d_num = 6 - each[5]
                driver_daily.get_url('https://pc.xuexi.cn/points/my-points.html')
                driver_daily.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
                category = driver_daily.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]').text() #get_attribute("name")

                tips = driver_daily._view_tips()
                if not tips:
                    print("本题没有提示")
                    if "填空题" == category:
                        return None
                    elif "多选题" == category:
                        return "ABCDEFG"[:len(options)]
                    elif "单选题" == category:
                        return self._search(content, options, excludes)
                    else:
                        print("题目类型非法")
                else:
                    if "填空题" == category:
                        dest = re.findall(r'.{0,2}\s+.{0,2}', content)
                        print(f'dest: {dest}')
                        if 1 == len(dest):
                            dest = dest[0]
                            print(f'单处填空题可以尝试正则匹配')
                            pattern = re.sub(r'\s+', '(.+?)', dest)
                            print(f'匹配模式 {pattern}')
                            res = re.findall(pattern, tips)
                            if 1 == len(res):
                                return res[0]
                        print(f'多处填空题难以预料结果，索性不处理')
                        return None

                    elif "多选题" == category:
                        check_res = [letter for letter, option in zip(letters, options) if option in tips]
                        if len(check_res) > 1:
                            print(f'根据提示，可选项有: {check_res}')
                            return "".join(check_res)
                        return "ABCDEFG"[:len(options)]
                    elif "单选题" == category:
                        radio_in_tips, radio_out_tips = "", ""
                        for letter, option in zip(letters, options):
                            if option in tips:
                                print(f'{option} in tips')
                                radio_in_tips += letter
                            else:
                                print(f'{option} out tips')
                                radio_out_tips += letter

                        print(f'含 {radio_in_tips} 不含 {radio_out_tips}')
                        if 1 == len(radio_in_tips) and radio_in_tips not in excludes:
                            print(f'根据提示 {radio_in_tips}')
                            return radio_in_tips
                        if 1 == len(radio_out_tips) and radio_out_tips not in excludes:
                            print(f'根据提示 {radio_out_tips}')
                            return radio_out_tips
                        return self._search(content, options, excludes)
                    else:
                        print("题目类型非法")

                    print("\r每日答题中，题目剩余{}题".format(d_log + d_num - i), end="")
                    time.sleep(1)
                    total, each = show_score(cookies)
                    if each[5] >= 6:
                        print("检测到每日答题分数已满,退出学习")
                        break
                d_log += d_num
            else:
                with open("./user/{}/d_log".format(uname), "w", encoding="utf8") as fp:
                    fp.write(str(d_log))
                break
        if try_count < 10:
            print("每日答题完成")
        else:
            print("每日答题出现异常，请检查用户名下d_log文件记录数")
        driver_daily.quit()
    else:
        print("每日答题之前学完了")


if __name__ == '__main__':
    #  0 读取版本信息
    start_time = time.time()
    info_shread = threads.MyThread("获取更新信息...", version.up_info)
    info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    dd_status, uname = user.get_user()
    cookies, a_log, v_log, d_log = user_flag(dd_status, uname)
    total, each = show_score(cookies)

    nohead, lock, stime = get_argv()
    '''
    article_thread = threads.MyThread("文章学习", article, cookies, a_log, each, lock=lock)
    video_thread = threads.MyThread("视频学习", video, cookies, v_log, each, lock=lock)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()'''
    daily(cookies, d_log, each)
    print("总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    user.shutdown(stime)
