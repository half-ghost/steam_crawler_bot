from bs4 import BeautifulSoup as bs
import re
from requests import get
import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "results")
TAG_PATH = os.path.join(os.path.dirname(__file__))


#根据爬取的网址返回生成json文件的路径和命名
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

#主爬虫程序
def crawler(url_choose):
    if not os.path.exists(FILE_PATH):
        os.mkdir(FILE_PATH)
    if os.path.exists(FILE_NAME(url_choose)):
        os.remove(FILE_NAME(url_choose))
    get_request = get(url_choose).content.decode()
    soup = bs(get_request.replace(r"\n", "").replace(r"\t", "").replace(r"\r", "").replace("\\", ""), "lxml")
    row_list = soup.find_all(name = "a", class_ = "search_result_row")
    title_list = []
    price_list = []
    href_list = []
    img_list = []
    for row in row_list:
        soup_list = bs(str(row), "lxml")
        #获取标题
        title = re.findall(r"<span class=\"title\">(.*?)</span>", str(row))
        title_list.append(title[0])
        #获取链接
        href = re.findall(r'href="(.*?)"', str(row))
        href_list.append(href[0])
        #获取缩略图链接
        img = re.findall(r"src=\"(.*?)\"", str(row))
        img_list.append(img[0])
        # res = get(str(img[0]).replace("capsule_sm_120", "header")).content
        # with open(os.path.join(IMG_PATH, str(row_list.index(row))) + ".jpg", 'wb') as f:
        #     f.write(res)
        #获取价格
        if str(soup_list.strike) == "None" :
            m = str(re.findall(r"<div class=\"col search_price responsive_secondrow\">(.*?)</div>", str(row))[0].replace(" ", ""))
            if "¥" in m:
                price_list.append(m)
            else:
                price_list.append("免费开玩")
        else:
            discount = re.findall(r"<br/>(.*?)  ", str(row))
            price_list.append(soup_list.strike.string.replace(" ", "") + " 折扣价为" + str(discount[0]).replace(" ", ""))
    
    
    result_dict = {}
    for i in title_list:
        index = title_list.index(i)
        result_dict["标题"] = title_list[index]
        result_dict["原价"] = price_list[index]
        result_dict["链接"] = href_list[index]
        result_dict["图片"] = img_list[index]
        with open(FILE_NAME(url_choose), "a", encoding="utf-8")as f:
            f.write(json.dumps(result_dict, ensure_ascii=False) + "\n")

#根据传入参数返回搜索页链接以及搜索的标签
def url_decide(tag, page):
    tag_search = "&tags="
    tag_name = ""
    tag_list = tag
    count = f"&start={(page-1)*50}&count=50"
    with open(os.path.join(TAG_PATH, "tag.json"), "r", encoding="utf-8")as f:
        for line in f.readlines():
            for i in tag_list:
                try:
                    tag_search += json.loads(line)[i] + ","
                    tag_name += i + ","
                except:
                    pass
    tag_search_url = "https://store.steampowered.com/search/results/?query&force_infinite=1&filter=topsellers&snr=1_7_7_7000_7&infinite=1" + tag_search.strip(",") + count
    return tag_search_url,tag_name