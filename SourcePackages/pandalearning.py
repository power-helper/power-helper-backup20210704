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
from pdlearn.mydriver import Mydriver


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
    # print("阅读文章:",each[0],"/6,观看视频:",each[1],"/6,登陆:",each[2],"/1,文章时长:",each[3],"/6,视频时长:",each[4],"/6,每日答题:",each[5],"/6,每周答题:",each[6],"/5,专项答题:",each[7],"/10")
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
                    readarticle_time = 60 + random.randint(5, 15)
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
                    watchvideo_time = 60 + random.randint(5, 15)
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


def check_delay():
    delay_time = random.randint(2, 5)
    print('等待 ', delay_time, ' 秒')
    time.sleep(delay_time)


def daily(cookies, d_log, each):
    if each[5] < 6:
        # driver_daily = mydriver.Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_daily = mydriver.Mydriver(nohead=False)
        driver_daily.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_daily.get_url("https://www.xuexi.cn/notFound.html")
        driver_daily.set_cookies(cookies)
        try_count = 0

        if each[5] < 6:
            d_num = 6 - each[5]
            letters = list("ABCDEFGHIJKLMN")
            driver_daily.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_daily.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
            while each[5] < 6:
                try:
                    category = driver_daily.xpath_getText(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]')  # get_attribute("name")
                except Exception as e:
                    print('查找元素失败！')
                    break
                print(category)
                tips = driver_daily._view_tips()
                check_delay()
                if not tips:
                    print("本题没有提示")
                    if "填空题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                    elif "多选题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                    elif "单选题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                    else:
                        print("题目类型非法")
                        break
                else:
                    if "填空题" in category:
                        answer = tips
                        driver_daily.fill_in_blank(answer)

                    elif "多选题" in category:
                        options = driver_daily.radio_get_options()
                        radio_in_tips, radio_out_tips = "", ""
                        for letter, option in zip(letters, options):
                            for tip in tips:
                                if tip in option:
                                    # print(f'{option} in tips')
                                    if letter not in radio_in_tips:
                                        radio_in_tips += letter
                                else:
                                    # print(f'{option} out tips')
                                    if letter not in radio_out_tips:
                                        radio_out_tips += letter

                        print('含 ', radio_in_tips, '不含', radio_out_tips)
                        if len(radio_in_tips) > 1:  # and radio_in_tips not in driver_daily.excludes:
                            print('根据提示', radio_in_tips)
                            driver_daily.radio_check(radio_in_tips)
                        elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_daily.radio_check(radio_out_tips)
                        # return driver_daily._search(content, options, excludes)
                        else:
                            print('无法根据提示判断，准备搜索……')
                    elif "单选题" in category:
                        options = driver_daily.radio_get_options()
                        radio_in_tips, radio_out_tips = "", ""
                        '''
                        option_elements = driver_daily.wait.until(driver_daily.EC.presence_of_all_elements_located(
                            (driver_daily.By.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]')))
                        # option_elements = self.find_elements(rules['challenge_options'])
                        options = [x.get_attribute("name") for x in option_elements]'''
                        for letter, option in zip(letters, options):
                            for tip in tips:
                                if tip in option:
                                    # print(f'{option} in tips')
                                    if letter not in radio_in_tips:
                                        radio_in_tips += letter
                                else:
                                    # print(f'{option} out tips')
                                    if letter not in radio_out_tips:
                                        radio_out_tips += letter

                        print('含 ', radio_in_tips, '不含', radio_out_tips)
                        if 1 == len(radio_in_tips):  # and radio_in_tips not in driver_daily.excludes:
                            print('根据提示', radio_in_tips)
                            driver_daily.radio_check(radio_in_tips)
                        elif 1 == len(radio_out_tips):  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_daily.radio_check(radio_out_tips)
                        # return driver_daily._search(content, options, excludes)
                        else:
                            print('无法根据提示判断，准备搜索……')
                    else:
                        print("题目类型非法")
                        break
                    # print("\r每日答题中，题目剩余{}题".format(d_log + d_num - i), end="")
                    time.sleep(1)
                d_log += d_num

            total, each = show_score(cookies)
            if each[5] >= 6:
                print("检测到每日答题分数已满,退出学习")
                driver_daily.quit()
        else:
            with open("./user/{}/d_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(d_log))
            # break
        try:
            driver_daily.quit()
        except Exception as e:
            print('……')
    else:
        print("每日答题之前学完了")


def weekly(cookies, d_log, each):
    if each[6] < 5:
        # driver_weekly = mydriver.Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_weekly = mydriver.Mydriver(nohead=False)
        driver_weekly.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_weekly.get_url("https://www.xuexi.cn/notFound.html")
        driver_weekly.set_cookies(cookies)
        try_count = 0

        if each[6] < 5:
            d_num = 6 - each[5]
            letters = list("ABCDEFGHIJKLMN")
            driver_weekly.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_weekly.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
            time.sleep(2)
            flag = 1
            for tem in range(0, 40):
                for tem2 in range(0, 5):
                    try:
                        temword = driver_weekly.driver.find_element_by_xpath(
                            '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                                tem2 + 1) + ']/button').text
                    except:
                        temword = ''
                    name_list = ["开始答题", "继续答题", "重新答题"]
                    if flag == 1 and (any(name in temword for name in name_list)):
                        driver_weekly.click_xpath(
                            '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                                tem2 + 1) + ']/button')
                        flag = 0
            while each[6] < 5 and try_count < 10:
                try:
                    category = driver_weekly.xpath_getText(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div[1]/div[1]')  # get_attribute("name")
                except Exception as e:
                    print('查找元素失败！')
                    break
                print(category)
                tips = driver_weekly._view_tips()
                check_delay()
                if not tips:
                    print("本题没有提示")
                    if "填空题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                    elif "多选题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                    elif "单选题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                    else:
                        print("题目类型非法")
                        break
                else:
                    if "填空题" in category:
                        answer = tips
                        driver_weekly.fill_in_blank(answer)

                    elif "多选题" in category:
                        options = driver_weekly.radio_get_options()
                        radio_in_tips, radio_out_tips = "", ""
                        for letter, option in zip(letters, options):
                            for tip in tips:
                                if tip in option:
                                    # print(f'{option} in tips')
                                    if letter not in radio_in_tips:
                                        radio_in_tips += letter
                                else:
                                    # print(f'{option} out tips')
                                    if letter not in radio_out_tips:
                                        radio_out_tips += letter

                        print('含 ', radio_in_tips, '不含', radio_out_tips)
                        if len(radio_in_tips) > 1:  # and radio_in_tips not in driver_weekly.excludes:
                            print('根据提示', radio_in_tips)
                            driver_weekly.radio_check(radio_in_tips)
                        elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_weekly.radio_check(radio_out_tips)
                        # return driver_weekly._search(content, options, excludes)
                        else:
                            print('无法根据提示判断，准备搜索……')
                    elif "单选题" in category:
                        options = driver_weekly.radio_get_options()
                        radio_in_tips, radio_out_tips = "", ""
                        '''
                        option_elements = driver_weekly.wait.until(driver_weekly.EC.presence_of_all_elements_located(
                            (driver_weekly.By.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]')))
                        # option_elements = self.find_elements(rules['challenge_options'])
                        options = [x.get_attribute("name") for x in option_elements]'''
                        for letter, option in zip(letters, options):
                            for tip in tips:
                                if tip in option:
                                    # print(f'{option} in tips')
                                    if letter not in radio_in_tips:
                                        radio_in_tips += letter
                                else:
                                    # print(f'{option} out tips')
                                    if letter not in radio_out_tips:
                                        radio_out_tips += letter

                        print('含 ', radio_in_tips, '不含', radio_out_tips)
                        if 1 == len(radio_in_tips):  # and radio_in_tips not in driver_weekly.excludes:
                            print('根据提示', radio_in_tips)
                            driver_weekly.radio_check(radio_in_tips)
                        elif 1 == len(radio_out_tips):  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_weekly.radio_check(radio_out_tips)
                        # return driver_weekly._search(content, options, excludes)
                        else:
                            print('无法根据提示判断，准备搜索……')
                    else:
                        print("题目类型非法")
                        break
                    # print("\r每周答题中，题目剩余{}题".format(d_log + d_num - i), end="")
                    time.sleep(1)
                d_log += d_num

            total, each = show_score(cookies)
            if each[6] >= 5:
                print("检测到每周答题分数已满,退出学习")
                driver_weekly.quit()
        else:
            with open("./user/{}/d_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(d_log))
            # break
        try:
            driver_weekly.quit()
        except Exception as e:
            print('……')
    else:
        print("每周答题之前学完了")


def zhuanxiang(cookies, d_log, each):
    if each[7] < 10:
        # driver_zhuanxiang = mydriver.Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_zhuanxiang = mydriver.Mydriver(nohead=False)
        driver_zhuanxiang.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_zhuanxiang.get_url("https://www.xuexi.cn/notFound.html")
        driver_zhuanxiang.set_cookies(cookies)
        try_count = 0

        if each[7] < 10:
            d_num = 10 - each[5]
            letters = list("ABCDEFGHIJKLMN")
            driver_zhuanxiang.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_zhuanxiang.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div')
            time.sleep(2)
            for tem in range(0, 40):
                try:
                    temword = driver_zhuanxiang.driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div/div/div/div[' + str(tem + 1) + ']/div[2]/button').text
                except:
                    temword = ''
                name_list = ["开始答题", "继续答题", "重新答题"]
                if (any(name in temword for name in name_list)):
                    driver_zhuanxiang.click_xpath(
                        '//*[@id="app"]/div/div[2]/div/div[4]/div/div/div/div[' + str(tem + 1) + ']/div[2]/button')
                    break
            while each[7] < 10:
                try:
                    category = driver_zhuanxiang.xpath_getText(
                        '//*[@id="app"]/div/div[2]/div/div[6]/div[1]/div[1]')  # get_attribute("name")
                except Exception as e:
                    print('查找元素失败！')
                    break
                print(category)
                tips = driver_zhuanxiang._view_tips()
                check_delay()
                if not tips:
                    print("本题没有提示")
                    if "填空题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                    elif "多选题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                    elif "单选题" in category:
                        print('没有找到提示，暂时略过')
                        continue
                        # return driver_daily._search(driver_daily.content, driver_daily.options, driver_daily.excludes)
                    else:
                        print("题目类型非法")
                        break
                else:
                    if "填空题" in category:
                        answer = tips
                        driver_zhuanxiang.zhuanxiang_fill_in_blank(answer)

                    elif "多选题" in category:
                        options = driver_zhuanxiang.radio_get_options()
                        radio_in_tips, radio_out_tips = "", ""
                        for letter, option in zip(letters, options):
                            for tip in tips:
                                if tip in option:
                                    # print(f'{option} in tips')
                                    if letter not in radio_in_tips:
                                        radio_in_tips += letter
                                else:
                                    # print(f'{option} out tips')
                                    if letter not in radio_out_tips:
                                        radio_out_tips += letter

                        print('含 ', radio_in_tips, '不含', radio_out_tips)
                        if len(radio_in_tips) > 1:  # and radio_in_tips not in driver_zhuanxiang.excludes:
                            print('根据提示', radio_in_tips)
                            driver_zhuanxiang.radio_check(radio_in_tips)
                        elif len(radio_out_tips) > 1:  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_zhuanxiang.radio_check(radio_out_tips)
                        # return driver_zhuanxiang._search(content, options, excludes)
                        else:
                            print('无法根据提示判断，准备搜索……')
                    elif "单选题" in category:
                        options = driver_zhuanxiang.radio_get_options()
                        radio_in_tips, radio_out_tips = "", ""
                        '''
                        option_elements = driver_zhuanxiang.wait.until(driver_zhuanxiang.EC.presence_of_all_elements_located(
                            (driver_zhuanxiang.By.XPATH, '//*[@id="app"]/div/div[2]/div/div[4]/div[1]')))
                        # option_elements = self.find_elements(rules['challenge_options'])
                        options = [x.get_attribute("name") for x in option_elements]'''
                        for letter, option in zip(letters, options):
                            for tip in tips:
                                if tip in option:
                                    # print(f'{option} in tips')
                                    if letter not in radio_in_tips:
                                        radio_in_tips += letter
                                else:
                                    # print(f'{option} out tips')
                                    if letter not in radio_out_tips:
                                        radio_out_tips += letter

                        print('含 ', radio_in_tips, '不含', radio_out_tips)
                        if 1 == len(radio_in_tips):  # and radio_in_tips not in driver_zhuanxiang.excludes:
                            print('根据提示', radio_in_tips)
                            driver_zhuanxiang.radio_check(radio_in_tips)
                        elif 1 == len(radio_out_tips):  # and radio_out_tips not in excludes
                            print('根据提示', radio_out_tips)
                            driver_zhuanxiang.radio_check(radio_out_tips)
                        # return driver_zhuanxiang._search(content, options, excludes)
                        else:
                            print('无法根据提示判断，准备搜索……')
                    else:
                        print("题目类型非法")
                        break
                    # print("\r专项答题中，题目剩余{}题".format(d_log + d_num - i), end="")
                    time.sleep(1)
                d_log += d_num

            total, each = show_score(cookies)
            if each[6] >= 5:
                print("检测到专项答题分数已满,退出学习")
                driver_zhuanxiang.quit()
        else:
            with open("./user/{}/d_log".format(uname), "w", encoding="utf8") as fp:
                fp.write(str(d_log))
            # break
        try:
            driver_zhuanxiang.quit()
        except Exception as e:
            print('……')
    else:
        print("专项答题之前学完了")


if __name__ == '__main__':
    #  0 读取版本信息
    start_time = time.time()

    print('''现支持以下模式：
    1 文章+视频
    2 每日答题+每周答题+专项答题+文章+视频
    3 每日答题+文章+视频''')
    TechXueXi_mode = input("请选择模式并回车： ")

    info_shread = threads.MyThread("获取更新信息...", version.up_info)
    info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    dd_status, uname = user.get_user()
    cookies, a_log, v_log, d_log = user_flag(dd_status, uname)
    total, each = show_score(cookies)
    nohead, lock, stime = get_argv()

    if TechXueXi_mode in ["2", "3"]:
        print('开始每日答题……')
        daily(cookies, d_log, each)
    if TechXueXi_mode in ["2"]:
        print('开始每周答题……')
        weekly(cookies, d_log, each)
        print('开始专项答题……')
        zhuanxiang(cookies, d_log, each)

    article_thread = threads.MyThread("文章学习", article, cookies, a_log, each, lock=lock)
    video_thread = threads.MyThread("视频学习", video, cookies, v_log, each, lock=lock)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()
    print("总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    user.shutdown(stime)
