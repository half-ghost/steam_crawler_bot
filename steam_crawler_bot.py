from bs4 import BeautifulSoup as bs
import re
from requests import get
import json
import os

from requests.models import stream_decode_response_unicode

TAG_PATH = os.path.join(os.path.dirname(__file__))

# steam爬虫程序
def crawler(url_choose):
    with open(os.path.join(TAG_PATH, "tag.json"), "r", encoding="utf-8")as f:
        data = json.loads(f.read())
    get_request = get(url_choose).content.decode()
    soup = bs(get_request.replace(r"\n", "").replace(r"\t", "").replace(r"\r", "").replace("\\", ""), "lxml")
    row_list = soup.find_all(name = "a", class_ = "search_result_row")
    title_list, price_list, href_list, img_list, rate_list, tag_list = [], [], [], [], [], []
    for row in row_list:
        soup_list = bs(str(row), "lxml")
        # 获取标题
        title = re.findall(r"<span class=\"title\">(.*?)</span>", str(row))
        title_list.append(title[0])
        # 获取链接
        href = re.findall(r'href="(.*?)"', str(row))
        href_list.append(href[0])
        # 获取缩略图链接
        img = re.findall(r"src=\"(.*?)\"", str(row))
        img_list.append(img[0])
        # 获取价格
        if str(soup_list.strike) == "None" :
            try:
                m = str(re.findall(r"<div class=\"col search_price responsive_secondrow\">(.*?)</div>", str(row))[0].replace(" ", ""))
            except:
                m = ("无价格信息")
                price_list.append(m)
            if "¥" in m:
                price_list.append(m)
            else:
                price_list.append("免费开玩")
        else:
            discount = re.findall(r"<br/>(.*?)  ", str(row))
            discount_percent = re.findall(r"<span>(.*?)</span>", str(row))
            price_list.append(f'{soup_list.strike.string.replace(" ", "")} 折扣价：{str(discount[0]).replace(" ", "")}({discount_percent[0]})')
        # 获取用户评价
        rate = re.findall(r"data-tooltip-html=\"(.*?)\">", str(row))
        try:
            rate_list.append(rate[0].replace("&lt;br&gt", "").replace(" ", ""))
        except:
            rate_list.append("暂无用户评测")
        # 获取标签
        tag = soup_list.a["data-ds-tagids"].strip("[]").split(",")
        tagk = ""
        for k,v in data["tag_dict"].items():
            for i in tag:
                if i == v:
                    tagk += k + ","
        tag_list.append(tagk.strip(","))
    
    mes_list = []
    for i in range(len(title_list)):
        mes = f"[CQ:image,file={img_list[i]}]\n{title_list[i]}\n原价：{price_list[i]}\n链接:{href_list[i]}\n{rate_list[i]}\n用户标签：{tag_list[i]}"
        data = {
        "type": "node",
        "data": {
            "name": "sbeam机器人",
            "uin": "2854196310",
            "content":mes
                }
            }
        mes_list.append(data)
    return mes_list

# 根据传入参数返回搜索页链接以及搜索的标签
def url_decide(tag, page):
    tag_search = "&tags="
    tag_name = ""
    tag_list = tag
    count = f"&start={(page-1)*50}&count=50"
    with open(os.path.join(TAG_PATH, "tag.json"), "r", encoding="utf-8")as f:
        data = json.loads(f.read())
        for i in tag_list:
            try:
                tag_search += data["tag_dict"][i] + ","
                tag_name += i + ","
            except:
                pass
    tag_search_url = "https://store.steampowered.com/search/results/?l=schinese&query&force_infinite=1&filter=topsellers&snr=1_7_7_7000_7&infinite=1" + tag_search.strip(",") + count
    return tag_search_url,tag_name

# 小黑盒数据爬虫
def hey_box(page):
    url1 = "https://api.xiaoheihe.cn/game/web/all_recommend/games/?os_type=web&version=999.0.0&show_type=discount&limit=30&offset=" + str((page-1)*30)
    res = get(url = url1).text
    json_page = json.loads(res)
    result = []
    announce = {
        "type": "node",
        "data": {
            "name": "sbeam机器人",
            "uin": "2854196310",
            "content":f"    ***数据来源于小黑盒官网***\n默认展示小黑盒steam促销页面"
                }
            }
    result.insert(0,announce)
    for i in range(30):
        # appid
        url = "https://store.steampowered.com/app/" + str(json_page["result"]["list"][i]["appid"])
        img = "https://media.st.dl.pinyuncloud.com/steam/apps/" + str(json_page["result"]["list"][i]["appid"]) + "/capsule_sm_120.jpg"
        # 名称
        title = json_page["result"]["list"][i]["game_name"]
        # 原价
        original = json_page["result"]["list"][i]["price"]["initial"]
        # 当前价
        current = json_page["result"]["list"][i]["price"]["current"]
        # 是否史低1是0否
        try:
            lowest = json_page["result"]["list"][i]["price"]["is_lowest"]
            discount = json_page["result"]["list"][i]["price"]["discount"]
        except:
            lowest = json_page["result"]["list"][i]["heybox_price"]["is_lowest"]
            discount = json_page["result"]["list"][i]["heybox_price"]["discount"]
        lowest_state = "是史低哦" if lowest == 1 else "不是史低哦"
        try:
            new_lowest = json_page["result"]["list"][i]["price"]["new_lowest"]
            newlowest = "好耶！是新史低！" if new_lowest == 1 else ""
        except:
            newlowest = ""
        # 截止日期
        try:
            deadline = json_page["result"]["list"][i]["price"]["deadline_date"]
        except:
            deadline = "无截止日期信息"
        mes = f"[CQ:image,file={img}]\n{title}\n原价:¥{original} 当前价:¥{current}(-{discount}%)\n{lowest_state}\n链接:{url}\n{deadline} {newlowest}".strip()
        data = {
        "type": "node",
        "data": {
            "name": "sbeam机器人",
            "uin": "2854196310",
            "content":mes
                }
            }
        result.append(data)
    return result

# 小黑盒搜索
def hey_box_search(game_name):
    url1 = "https://api.xiaoheihe.cn/game/search/?os_type=web&version=999.0.0&q=" + game_name
    res = get(url = url1).text
    json_page = json.loads(res)
    result = []
    announce = {
        "type": "node",
        "data": {
            "name": "sbeam机器人",
            "uin": "2854196310",
            "content":f"***数据来源于小黑盒官网***\n游戏{game_name}搜索结果如下"
                }
            }
    result.insert(0,announce)
    for i in range(len(json_page["result"]["games"])):
        steamappid = str(json_page["result"]["games"][i]["steam_appid"])
        # 名称
        name = json_page["result"]["games"][i]["name"]
        # 图片
        img = "https://media.st.dl.pinyuncloud.com/steam/apps/" + steamappid + "/capsule_sm_120.jpg"
        img1 = json_page["result"]["games"][i]["image"]        
        # 获取平台信息
        try:
            platform = json_page["result"]["games"][i]["platforms"]
            if "steam" in platform:
                url = "https://store.steampowered.com/app/" + steamappid
                # 原价
                original = json_page["result"]["games"][i]["price"]["initial"]
                # 当前价
                current = json_page["result"]["games"][i]["price"]["current"]
                try:
                    lowestprice = "平史低:¥" + str(json_page["result"]["games"][i]["price"]["lowest_price"])
                except:
                    lowestprice = "无平史低信息"
                if original != current:
                    lowest = json_page["result"]["games"][i]["price"]["is_lowest"]
                    discount = json_page["result"]["games"][i]["price"]["discount"]
                    lowest_state = "是史低哦" if lowest == 1 else "不是史低哦"
                    try:
                        new_lowest = json_page["result"]["games"][i]["price"]["new_lowest"]
                        newlowest = "好耶！是新史低！" if new_lowest == 1 else ""
                    except:
                        newlowest = ""
                    # 截止日期
                    try:
                        deadline = json_page["result"]["games"][i]["price"]["deadline_date"]
                    except:
                        deadline = "无截止日期信息"
                    mes = f"[CQ:image,file={img}]\n{name}\n原价:¥{original} 当前价:¥{current}(-{discount}%)\n{lowestprice} {lowest_state}\n链接:{url}\n{deadline} {newlowest}".strip()
                else:
                    mes = f"[CQ:image,file={img}]\n{name}\n当前无打折信息\n当前价:¥{current} {lowestprice}\n链接:{url}"
            else:
                platform = "非steam平台,不进行解析,请自行查看链接"
                url = "https://www.xiaoheihe.cn/games/detail/" + steamappid
                mes = f"[CQ:image,file={img1}]\n{name}\n{platform}\n链接{url}"
        except:
            platform = "非steam平台,不进行解析,请自行查看链接"
            url = "https://www.xiaoheihe.cn/games/detail/" + steamappid
            mes = f"[CQ:image,file={img1}]\n{name}\n{platform}\n链接{url}"
        data = {
        "type": "node",
        "data": {
            "name": "sbeam机器人",
            "uin": "2854196310",
            "content":mes
                }
            }
        result.append(data)
    return result
