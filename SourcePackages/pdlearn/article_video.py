import time
import random
from pdlearn import get_links
from pdlearn.mydriver import Mydriver
from pdlearn.score import show_score
from pdlearn.const import const


def article(cookies, a_log, scores):
    if scores["article_num"] < const.article_num_all or scores["article_time"] < const.article_time_all:
        # driver_article = Mydriver(nohead=nohead)
        driver_article = Mydriver(nohead=True)
        driver_article.get_url("https://www.xuexi.cn/notFound.html")
        driver_article.set_cookies(cookies)
        links = get_links.get_article_links()
        try_count = 0
        readarticle_time = 0
        while True:
            if scores["article_num"] < const.article_num_all and try_count < 10:
                a_num = const.article_num_all - scores["article_num"]
                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    readarticle_time = 60 + random.randint(5, 15)
                    for j in range(readarticle_time):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                        print("\r文章数量学习中，文章剩余{}篇,本篇剩余时间{}秒".format(a_log + a_num - i, readarticle_time - j), end="")
                        time.sleep(1)
                    driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, scores = show_score(cookies)
                    if scores["article_num"] >= const.article_num_all:
                        print("检测到文章数量分数已满,退出学习")
                        break
                a_log += a_num
            else:
                with open("./user/{}/a_log".format(1), "w", encoding="utf8") as fp:
                    fp.write(str(a_log))
                break
        try_count = 0
        while True:
            if scores["article_time"] < const.article_time_all and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log - 1])
                remaining = (const.article_time_all - scores["article_time"]) * 1 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (60) == 0 and i != remaining:
                        total, scores = show_score(cookies)
                        if scores["article_time"] >= const.article_time_all:
                            print("检测到文章时长分数已满,退出学习")
                            break
                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, scores = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("文章学习完成")
        else:
            print("文章学习出现异常，请检查用户名下a_log文件记录数")
        driver_article.quit()
    else:
        print("文章之前学完了")


def video(cookies, v_log, scores):
    if scores["video_num"] < const.video_num_all or scores["video_time"] < const.video_time_all:
        # driver_video = Mydriver(nohead=nohead)
        driver_video = Mydriver(nohead=True)
        driver_video.get_url("https://www.xuexi.cn/notFound.html")
        driver_video.set_cookies(cookies)
        links = get_links.get_video_links()
        try_count = 0
        watchvideo_time = 0
        while True:
            if scores["video_num"] < const.video_num_all and try_count < 10:
                v_num = const.video_num_all - scores["video_num"]
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    watchvideo_time = 60 + random.randint(5, 15)
                    for j in range(watchvideo_time):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                        print("\r视频数量学习中，视频剩余{}个,本次剩余时间{}秒".format(v_log + v_num - i, watchvideo_time - j), end="")
                        time.sleep(1)
                    driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, scores = show_score(cookies)
                    if scores["video_num"] >= const.video_num_all:
                        print("检测到视频数量分数已满,退出学习")
                        break
                v_log += v_num
            else:
                with open("./user/{}/v_log".format(1), "w", encoding="utf8") as fp:
                    fp.write(str(v_log))
                break
        try_count = 0
        while True:
            if scores["video_time"] < const.video_time_all and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log - 1])
                remaining = (const.video_time_all - scores["video_time"]) * 1 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r视频时长学习中，视频总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (60) == 0 and i != remaining:
                        total, scores = show_score(cookies)
                        if scores["video_time"] >= const.video_time_all:
                            print("检测到视频时长分数已满,退出学习")
                            break
                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, scores = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("视频学习完成")
        else:
            print("视频学习出现异常，请检查用户名下v_log文件记录数")
        driver_video.quit()
    else:
        print("视频之前学完了")
