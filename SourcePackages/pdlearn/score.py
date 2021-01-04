import requests
from requests.cookies import RequestsCookieJar
import json

# 总积分
# https://pc-api.xuexi.cn/open/api/score/get?_t=1608769882241
# 今日积分
# https://pc-api.xuexi.cn/open/api/score/today/query

def get_score(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total_json = requests.get("https://pc-api.xuexi.cn/open/api/score/get", cookies=jar,
                             headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
        total = int(json.loads(total_json)["data"]["score"])
        score_json = requests.get("https://pc-api.xuexi.cn/open/api/score/today/queryrate", cookies=jar,
                             headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
        today_json = requests.get("https://pc-api.xuexi.cn/open/api/score/today/query", cookies=jar,
                             headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
        today = 0
        today = int(json.loads(today_json)["data"]["score"])
        dayScoreDtos = json.loads(score_json)["data"]["dayScoreDtos"]
        rule_list = [1, 2, 9, 1002, 1003, 6, 5, 4]
        score_list= [0, 0, 0, 0   , 0   , 0, 0, 0, 0, 0] # 长度为十
        for i in dayScoreDtos:
            for j in range(len(rule_list)):
                if i["ruleId"] == rule_list[j]:
                    score_list[j] = int(i["currentScore"])
        # 阅读文章，视听学习，登录，文章时长，视听学习时长，每日答题，每周答题，专项答题
        today = 0
        for i in dayScoreDtos:
            if(i["ruleId"] == 15 and int(i["currentScore"]) >= 1):
                today += 1
            else:
                today += int(i["currentScore"])
        scores = {}
        scores["article_num"]  = score_list[0] # 0阅读文章
        scores["video_num"]    = score_list[1] # 1视听学习
        scores["login"]        = score_list[2] # 7登录
        scores["article_time"] = score_list[3] # 6文章时长
        scores["video_time"]   = score_list[4] # 5视听学习时长
        scores["daily"]        = score_list[5] # 2每日答题
        scores["weekly"]       = score_list[6] # 3每周答题
        scores["zhuanxiang"]   = score_list[7] # 4专项答题
        
        scores["today"]        = today         # 8今日得分
        return total, scores
    except:
        print("=" * 60)
        print("get_video_links获取失败")
        print("=" * 60)
        raise
