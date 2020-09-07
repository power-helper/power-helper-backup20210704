import time
from sys import argv
import random
from pdlearn import version
from pdlearn import user
from pdlearn import user_agent
from pdlearn import dingding
from pdlearn import mydriver
from pdlearn import score
from pdlearn import threads
from pdlearn import get_links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def user_flag(dd_status, uname):

    if False and dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        #if (input("是否保存钉钉帐户密码，保存后可后免登陆学习(Y/N) ")) not in ["y", "Y"]:
        if True:
            driver_login = mydriver.Mydriver(nohead=False)
            cookies = driver_login.login()
        else:
            cookies = dingding.dd_login_status(uname)
    a_log = user.get_a_log(uname)
    v_log = user.get_v_log(uname)
    zx_log = user.get_zx_log(uname)
    mr_log = user.get_mr_log(uname)
    driver_login.quit()
    return cookies, a_log, v_log,zx_log,mr_log



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
    print("阅读文章:{}/6,观看视频:{}/6,专项答题:{}/10,每周答题:{}/5,每日答题:{}/6,登陆:{}/1,文章时长:{}/6,视频时长:{}/6".format(*each))
    return total, each


def article(cookies, a_log, each):
    if each[0] < 6 or each[6] < 6:
        driver_article = mydriver.Mydriver(nohead=nohead)
        driver_article.get_url("https://www.xuexi.cn/notFound.html")
        driver_article.set_cookies(cookies)
        links = get_links.get_article_links()
        try_count = 0
        while True:
            if each[0] < 6 and try_count < 10:
                a_num = 6 - each[0]
                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(120):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                        print("\r文章学习中，文章剩余{}篇,本篇剩余时间{}秒".format(a_log + a_num - i, 120 - j), end="")
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
            if each[6] < 6 and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log-1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each[3]) * 4 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (120) == 0 and i != remaining:
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
    if each[1] < 6 or each[7] < 6:
        driver_video = mydriver.Mydriver(nohead=nohead)
        driver_video.get_url("https://www.xuexi.cn/notFound.html")
        driver_video.set_cookies(cookies)
        links = get_links.get_video_links()
        try_count = 0
        while True:
            if each[1] < 6 and try_count < 10:
                v_num = 6 - each[1]
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(180):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                        print("\r视频学习中，视频剩余{}个,本次剩余时间{}秒".format(v_log + v_num - i, 180 - j), end="")
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
            if each[7] < 6 and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log-1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each[4]) * 3 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r视频学习中，视频总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (180) == 0 and i != remaining:
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
def zuoti(type,browser):
    flag = False
    time.sleep(5)
    daihao="4"
    if(type=="专项答题"):
        daihao="6"
    tixing = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[1]/div[1]').text
    try:
        browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[1]/div[3]/span').click()
    except:
        browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[1]/div[4]/span').click()

    for k in range(1):
        try:
            browser.execute_script('document.getElementsByClassName("ant-popover ant-popover-placement-bottom")[0].style.display="BLOCK"')
        except:
            continue
    time.sleep(10)
    temp_list = browser.find_elements_by_tag_name('font')
    answer_list=[]
    for k in temp_list:
        answer_list.append(k.text)
    Normal_answer=answer_list[0]
    daanlist = browser.find_elements_by_class_name('q-answer.choosable')
    browser.execute_script(
        'document.getElementsByClassName("ant-popover ant-popover-placement-bottom")[0].style.display="None"')
    if (tixing == "填空题" or tixing=="填空题（本道题10分）"):
        browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[1]/div[2]/div/input').send_keys(
            Normal_answer)
    if (tixing == "单选题" or tixing=="单选题（本道题10分）"):
        for k in daanlist:
            if(k.text.split(". ")[1] ==Normal_answer):
                flag=True
                k.click()
            break
        if(flag==False):
            daanlist[0].click()
    if (tixing == "多选题" or tixing=="多选题（本道题10分）"):
        timu = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[1]/div[2]/div').text
        a = timu.count('（）')
        b = len(daanlist)
        if (a == b):
            for k in daanlist:
                k.click()
        else:
            for k in daanlist:
                for l in answer_list:
                    if (k.text.split(". ")[1] == l):
                        k.click()
                        break

    time.sleep(5)
    butt = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[2]/button')
    butt.click()
    daanjiexi = browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[3]/div/div[1]')
    if (len(daanjiexi) >= 1):
        butt = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div['+daihao+']/div[2]/button')
        butt.click()
def zhuanxiangdati(cookies, zx_log, each):
    if each[2] < 10:
        options = Options()
        options.add_argument('--user-agent={}'.format(user_agent.getheaders()))
        driver_article = webdriver.Chrome(options=options)
        driver_article = webdriver.Chrome()
        driver_article.get("https://www.xuexi.cn/notFound.html")
        driver_article.delete_all_cookies()
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver_article.add_cookie({k: cookie[k] for k in cookie.keys()})
        links = 'https://pc.xuexi.cn/points/exam-paper-list.html'
        driver_article.get(links)
        time.sleep(5)
        buttons = driver_article.find_elements_by_xpath('//button/span[contains(text(), "开始答题")]')
        if (len(buttons) == 0):
            print("所有专项答题已完成")
        else:
            driver_article.execute_script("arguments[0].click();", buttons[0])
            time.sleep(4)
            for i in range(10):
                zuoti("专项答题",driver_article)
            driver_article.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[6]/div[2]/button[2]').click()
            print("专项答题已做完")
            driver_article.quit()
    else:
        print("专项答题已做完")
def meiridati(cookies, mr_log, each):
    print("正在做每日答题")
    if each[4] < 6:
        options = Options()
        options.add_argument('--user-agent={}'.format(user_agent.getheaders()))
        driver_article = webdriver.Chrome(options=options)
        driver_article = webdriver.Chrome()
        driver_article.get("https://www.xuexi.cn/notFound.html")
        driver_article.delete_all_cookies()
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver_article.add_cookie({k: cookie[k] for k in cookie.keys()})
        links = 'https://pc.xuexi.cn/points/exam-practice.html'
        driver_article.get(links)
        time.sleep(5)
        for i in range(5):
            zuoti("每日答题",driver_article)
        time.sleep(5)
        print("每日答题完成")
        driver_article.quit()
        # result = driver_article.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div/div/div[1]/div[2]').text
    else:
        print("每日答题已做完")
def weekdati(cookies, mr_log, each):
    print("正在做每周答题")
    if each[3] < 5:
        options = Options()
        options.add_argument('--user-agent={}'.format(user_agent.getheaders()))
        driver_article = webdriver.Chrome(options=options)
        driver_article.get("https://www.xuexi.cn/notFound.html")
        driver_article.delete_all_cookies()
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver_article.add_cookie({k: cookie[k] for k in cookie.keys()})
        links = 'https://pc.xuexi.cn/points/exam-weekly-list.html'
        driver_article.get(links)
        time.sleep(5)
        buttons = driver_article.find_elements_by_xpath('//button/span[contains(text(), "开始答题")]')
        if (len(buttons) == 0):
            print("每周答题已完成")
        else:
            driver_article.execute_script("arguments[0].click();", buttons[0])
            time.sleep(10)
            for i in range(5):
                zuoti("每周答题",driver_article)
        time.sleep(5)
        print("每周答题完成")
        driver_article.quit()
        # result = driver_article.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[4]/div/div/div[1]/div[2]').text
    else:
        print("每日答题已做完")
if __name__ == '__main__':
    #  0 读取版本信息
    start_time = time.time()
    # info_shread = threads.MyThread("获取更新信息...", version.up_info)
    # info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    dd_status, uname = user.get_user()
    cookies, a_log, v_log ,zx_log,mr_log = user_flag(dd_status, uname)
    total, each = show_score(cookies)

    nohead, lock, stime = get_argv()
    article_thread = threads.MyThread("文章学习", article, cookies, a_log, each, lock=lock)
    video_thread = threads.MyThread("视频学习", video, cookies, v_log, each, lock=lock)
    zx_thread = threads.MyThread("专项答题",zhuanxiangdati,cookies,zx_log,each,lock=lock)
    article_thread.start()
    video_thread.start()
    zx_thread.start()
    article_thread.join()
    video_thread.join()
    zx_thread.join()
    meiridati(cookies,mr_log,each)
    weekdati(cookies,mr_log,each)
    print("总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    user.shutdown(stime)
    exit()
