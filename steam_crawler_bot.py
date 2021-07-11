from bs4 import BeautifulSoup as bs
import re
from requests import get
import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "results")
TAG_PATH = os.path.join(os.path.dirname(__file__))

# 根据爬取的网址返回生成json文件的路径和命名
def FILE_NAME(url_check):
    if "Released_DESC" in url_check:
        NAME = os.path.join(FILE_PATH, 'new_result.json')
    elif "specials" in url_check:
        NAME = os.path.join(FILE_PATH, 'specials_result.json')
    elif "tags" in url_check:
        NAME = os.path.join(FILE_PATH, f"search_tag={re.findall(r'tags=(.*?)&start', url_check)[0]}.json")
    elif "term" in url_check:
        NAME = os.path.join(FILE_PATH, f"search_term={url_check[url_check.find('term=')+5 :]}.json")
    return NAME

# 主爬虫程序
def crawler(url_choose):
    if not os.path.exists(FILE_PATH):
        os.mkdir(FILE_PATH)
    if os.path.exists(FILE_NAME(url_choose)):
        os.remove(FILE_NAME(url_choose))
    with open(os.path.join(TAG_PATH, "tag2.json"), "r", encoding="utf-8")as f:
        data = json.loads(f.read())
    get_request = get(url_choose).content.decode()
    soup = bs(get_request.replace(r"\n", "").replace(r"\t", "").replace(r"\r", "").replace("\\", ""), "lxml")
    row_list = soup.find_all(name = "a", class_ = "search_result_row")
    title_list = []
    price_list = []
    href_list = []
    img_list = []
    rate_list = []
    tag_list = []
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
    
    result_dict = {}
    for i in title_list:
        index = title_list.index(i)
        result_dict["标题"] = title_list[index]
        result_dict["原价"] = price_list[index]
        result_dict["链接"] = href_list[index]
        result_dict["图片"] = img_list[index]
        result_dict["评测"] = rate_list[index]
        result_dict["标签"] = tag_list[index]
        with open(FILE_NAME(url_choose), "a", encoding="utf-8")as f:
            f.write(json.dumps(result_dict, ensure_ascii=False) + "\n")

# 根据传入参数返回搜索页链接以及搜索的标签
def url_decide(tag, page):
    tag_search = "&tags="
    tag_name = ""
    tag_list = tag
    count = f"&start={(page-1)*50}&count=50"
    with open(os.path.join(TAG_PATH, "tag2.json"), "r", encoding="utf-8")as f:
        data = json.loads(f.read())
        for i in tag_list:
            try:
                tag_search += data["tag_dict"][i] + ","
                tag_name += i + ","
            except:
                pass
    tag_search_url = "https://store.steampowered.com/search/results/?query&force_infinite=1&filter=topsellers&snr=1_7_7_7000_7&infinite=1" + tag_search.strip(",") + count
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
            "content":"***数据来源于小黑盒官网***"
                }
            }
    result.insert(0,announce)
    for i in range(30):
        # appid
        href = "https://store.steampowered.com/app/" + str(json_page["result"]["list"][i]["appid"])
        img = "https://media.st.dl.pinyuncloud.com/steam/apps/" + str(json_page["result"]["list"][i]["appid"]) + "/capsule_sm_120.jpg"
        # 名称
        title = json_page["result"]["list"][i]["game_name"]
        # 原价
        original = json_page["result"]["list"][i]["price"]["initial"]
        # 当前价
        current = json_page["result"]["list"][i]["price"]["current"]
        # 是否史低1是0否
        try:
            lowest = json_page["result"]["list"][i]["heybox_price"]["is_lowest"]
        except:
            lowest = json_page["result"]["list"][i]["price"]["is_lowest"]
        if lowest == 1:
            lowest_state = "是史低哦"
        else:
            lowest_state = "不是史低哦"
        new_lowest = json_page["result"]["list"][i]["price"]["new_lowest"]
        if new_lowest == 1:
            newlowest = "好耶！是新史低！"
        else:
            newlowest = ""
        mes = f"[CQ:image,file={img}]\n{title}\n原价:¥{original} 当前价:¥{current} {lowest_state}\n链接:{href}\n{newlowest}\n".strip()
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
