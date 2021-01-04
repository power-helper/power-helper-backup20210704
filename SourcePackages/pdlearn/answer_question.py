import time
from pdlearn.mydriver        import Mydriver
from pdlearn.score           import show_score

def daily(cookies, d_log, scores):
    if scores["daily"] < 5:
        # driver_daily = Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_daily = Mydriver(nohead=False)
        driver_daily.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_daily.get_url("https://www.xuexi.cn/notFound.html")
        driver_daily.set_cookies(cookies)
        try_count = 0

        if scores["daily"] < 5:
            d_num = 5 - scores["daily"]
            letters = list("ABCDEFGHIJKLMN")
            driver_daily.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_daily.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
            while scores["daily"] < 5:
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
                        radio_out_tips = [letter for letter, option in zip(letters, options) if
                                          (letter not in radio_in_tips)]

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
                        if '因此本题选' in tips:
                            check=[x for x in letters if x in tips]
                            driver_daily.radio_check(check)
                        else:
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

            total, scores = show_score(cookies)
            if scores["daily"] >= 5:
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


def weekly(cookies, d_log, scores):
    if scores["weekly"] < 5:
        # driver_weekly = Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_weekly = Mydriver(nohead=False)
        driver_weekly.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_weekly.get_url("https://www.xuexi.cn/notFound.html")
        driver_weekly.set_cookies(cookies)
        try_count = 0

        if scores["weekly"] < 5:
            d_num = 6 - scores["weekly"]
            letters = list("ABCDEFGHIJKLMN")
            driver_weekly.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_weekly.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
            time.sleep(2)
#<<<<<<< fix-some-bugs
#           flag = 1
#           for tem in range(0, 40):
#               for tem2 in range(0, 5):
#                   try:
#                       temword = driver_weekly.driver.find_element_by_xpath(
#                           '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
#                               tem2 + 1) + ']/button').text
#                   except:
#                       temword = ''
#                   name_list = ["开始答题", "继续答题"]
#                   if flag == 1 and (any(name in temword for name in name_list)):
#                       driver_weekly.click_xpath(
#                           '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
#                               tem2 + 1) + ']/button')
#                       flag = 0
            dati = driver_weekly.driver.find_elements_by_css_selector("#app .month .week button")
            toclick = dati
            for i in range(len(dati)-1,0,-1):
                j=dati[i]
                if("重新" in j.text or "满分" in j.text):
                    continue
                else:
                    toclick = j
                    break
            toclick.click()
            while scores["weekly"] < 5 and try_count < 10:
'''                
=======
            flag = 1
            page_num = 1
            last_page = int(driver_weekly.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[5]/ul/li[last()-1]/a').text)
            while page_num < last_page and flag == 1:
                print('进入每周答题第'+ str(page_num) +'页')
                all_month = len(driver_weekly.driver.find_elements_by_class_name('month'))
                cur_month = 1
                for tem in range(0, all_month):
                    for tem2 in range(0, 6):
                        if flag == 0:
                            break
                        try:
                            temword = driver_weekly.driver.find_element_by_xpath(
                                '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                                    tem2 + 1) + ']/button').text
                        except:
                            temword = ''
                            if all_month == cur_month:
                                driver_weekly.click_xpath(
                                        '//*[@id="app"]/div/div[2]/div/div[5]/ul/li[' + str(page_num + 2) + ']')
                                print('切换至下一页')
                                page_num += 1
                                time.sleep(2)
                            cur_month += 1
                            break
                        name_list = ["开始答题", "继续答题"]
                        if flag == 1 and (any(name in temword for name in name_list)):
                            driver_weekly.click_xpath(
                                '//*[@id="app"]/div/div[2]/div/div[4]/div/div[' + str(tem + 1) + ']/div[2]/div[' + str(
                                    tem2 + 1) + ']/button')
                            flag = 0
                        elif '重新答题' in temword:
                            continue
            while each[6] < 5 and try_count < 10:
>>>>>>> dev
'''
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
                        radio_out_tips = [letter for letter, option in zip(letters, options) if
                                          (letter not in radio_in_tips)]

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
                        if '因此本题选' in tips:
                            check=[x for x in letters if x in tips]
                            driver_weekly.radio_check(check)
                        else:
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

            total, scores = show_score(cookies)
            if scores["weekly"] >= 5:
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


def zhuanxiang(cookies, d_log, scores):
    if scores["zhuanxiang"] < 10:
        # driver_zhuanxiang = Mydriver(nohead=nohead)  time.sleep(random.randint(5, 15))
        driver_zhuanxiang = Mydriver(nohead=False)
        driver_zhuanxiang.driver.maximize_window()
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        print('请保持窗口最大化')
        driver_zhuanxiang.get_url("https://www.xuexi.cn/notFound.html")
        driver_zhuanxiang.set_cookies(cookies)
        try_count = 0

        if scores["zhuanxiang"] < 10:
            d_num = 10 - scores["zhuanxiang"]
            letters = list("ABCDEFGHIJKLMN")
            driver_zhuanxiang.get_url('https://pc.xuexi.cn/points/my-points.html')
            driver_zhuanxiang.click_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div')
            time.sleep(2)
#           for tem in range(0, 40):
#               try:
#                   temword = driver_zhuanxiang.driver.find_element_by_xpath(
#                       '//*[@id="app"]/div/div[2]/div/div[4]/div/div/div/div[' + str(tem + 1) + ']/div[2]/button').text
#               except:
#                   temword = ''
#               name_list = ["开始答题", "继续答题"]  # , "重新答题"
#               if (any(name in temword for name in name_list)):
#                   driver_zhuanxiang.click_xpath(
#                       '//*[@id="app"]/div/div[2]/div/div[4]/div/div/div/div[' + str(tem + 1) + ']/div[2]/button')
#                   break
            dati = driver_zhuanxiang.driver.find_elements_by_css_selector("#app .items .item button")
            toclick = dati
            #print("专项答题列表长度：",len(toclick))
            for i in range(len(dati)-1,-1,-1): # 从最后一个遍历到第一个
                j=dati[i]
                if("重新" in j.text or "满分" in j.text):
                    continue
                else:
                    toclick = j
                    toclick.click()
                    break
                    


            while scores["zhuanxiang"] < 10:
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
                        radio_out_tips = [letter for letter, option in zip(letters, options) if
                                          (letter not in radio_in_tips)]

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
                        if '因此本题选' in tips:
                            check=[x for x in letters if x in tips]
                            driver_zhuanxiang.radio_check(check)
                        else:
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

            total, scores = show_score(cookies)
            if scores["zhuanxiang"] >= 5:
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

