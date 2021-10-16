from bs4 import BeautifulSoup as bs
from requests import get
import os

FILE_PATH = os.path.join(os.path.dirname(__file__))
head = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 \
    (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36"}

def xjy_compare():
    xjy_url = "https://www.ithome.com/tag/xijiayi"
    try:
        xjy_page = get(url = xjy_url, headers=head).text
        soup = bs(xjy_page, "lxml")
        url_new = []
        for xjy_info in soup.find_all(name = "a", class_ = "title"):
            info_soup = bs(str(xjy_info), "lxml")
            url_new.append(info_soup.a["href"])
        if url_new == []:
            return "Server Error"
        else:
            if os.path.exists(os.path.join(FILE_PATH, "xjy_result.txt")) == False:
                with open(os.path.join(FILE_PATH, "xjy_result.txt"), "w+", encoding="utf-8")as f:
                    for i in url_new:
                        f.write(i + "\n")
            url_old = []
            with open(os.path.join(FILE_PATH, "xjy_result.txt"), "r+", encoding="utf-8")as f:
                for i in f.readlines():
                    url_old.append(i.strip())
            seta = set(url_new)
            setb = set(url_old)
            compare_list = list(seta-setb)
            with open(os.path.join(FILE_PATH, "xjy_result.txt"), "w+", encoding="utf-8")as f:
                for i in url_new:
                        f.write(i + "\n")
    except Exception as e:
        compare_list.append(f"error:{e}")
    return compare_list

def xjy_result(model,compare_list):
    result_text_list = []
    xjy_list = []
    if model == "Default":
        xjy_list = compare_list
    elif model == "Query":
        with open(os.path.join(FILE_PATH, "xjy_result.txt"), "r+", encoding="utf-8")as f:
            lines_list = f.readlines()
            for i in lines_list:
                xjy_list.append(i.strip())
                if lines_list.index(i) == compare_list-1:
                    break
    try:
        for urls in xjy_list:
            page = get(url= urls,headers= head).text
            soup = bs(page, "lxml")
            info_soup = bs(str(soup.find(name = "div", class_ = "post_content")), "lxml").find_all(name = "p")
            second_text = ""
            for i in info_soup:
                if i.a != None:
                    if i.a['href'] == "https://www.ithome.com/":
                        text = i.text + "|"
                    elif i.a.get('class') == 's_tag':
                        text = ""
                    else:
                        text = i.a["href"] + "|"
                    first_text = text
                else:
                    first_text = i.text + "|"
                second_text += first_text.replace("\xa0", " ")
            third_text = second_text.split("|")
            url_text = "未检测到领取地址"
            for part in third_text:
                if "http" in part:
                    url_text += "领取地址:" + part + "\n"
            final_text = f"{third_text[0]}......(更多内容请阅读原文)\n{url_text.replace('未检测到领取地址', '')}"
            result_text_list.append(final_text + f"原文地址:{urls}")
    except Exception as e:
        result_text_list = f"error:{e}"
    return result_text_list
