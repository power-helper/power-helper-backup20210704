import requests
from requests.cookies import RequestsCookieJar
import json


def get_score(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total = requests.get("https://pc-api.xuexi.cn/open/api/score/get", cookies=jar,
                             headers={'Cache-Control': 'no-cache'}).content.decode("utf8")
        total = int(json.loads(total, encoding="utf8")["data"]["score"])
        each1 = requests.get("https://pc-api.xuexi.cn/open/api/score/today/queryrate", cookies=jar,
                             headers={'Cache-Control': 'no-cache'}).content.decode(
            "utf8")
        each1 = json.loads(each1, encoding="utf8")["data"]["dayScoreDtos"]
        each1 = [int(i["currentScore"]) for i in each1 if i["ruleId"] in [1, 2, 9, 1002, 1003, 6, 5, 4]]
        each = [0, 0, 0, 0, 0, 0, 0, 0]
        each[0] = each1[0]
        each[1] = each1[1]
        each[2] = each1[5]
        each[3] = each1[6]
        each[4] = each1[7]
        each[5] = each1[4]
        each[6] = each1[3]
        each[7] = each1[2]
        return total, each
    except:
        print("=" * 120)
        print("get_video_links获取失败")
        print("=" * 120)
        raise
