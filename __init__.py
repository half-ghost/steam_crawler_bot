from hoshino import Service
from .new import crawler,FILE_NAME,url_decide
import json
import os

sv = Service("stbot")
url_new = "https://store.steampowered.com/search/results/?l=schinese&query&dynamic_data=&sort_by=Released_DESC&snr=1_7_7_230_7&category1=998&os=win&infinite=1&start=0&count=50"
url_specials = "https://store.steampowered.com/search/results/?l=schinese&query&sort_by=_ASC&category1=998&specials=1&filter=topsellers&start=0&count=50"
FILE_PATH = os.path.dirname(__file__)

#匹配关键词发送相关信息，例：今日特惠，发送今日特惠信息，今日新品则发送新品信息
@sv.on_prefix('今日')
async def Gameinfo(bot, ev):
    model = ev.message.extract_plain_text().strip()
    if model == "新品":
        open_file = FILE_NAME(url_new)
        if not os.path.exists(open_file):
            await bot.send(ev, "正在抓取...")
            try:
                crawler(url_new)
            except:
                await bot.send(ev, "哦吼，出错了，请检查运行日志或者稍后再试")
    elif model == "特惠":
        open_file = FILE_NAME(url_specials)
        if not os.path.exists(open_file):
            await bot.send(ev, "正在抓取...")
            try:
                crawler(url_specials)
            except:
                await bot.send(ev, "哦吼，出错了，请检查运行日志或者稍后再试")
    mes_list = []
    try:
        with open(open_file, "r", encoding="utf-8")as f:
            for line in f.readlines():
                result_dict = json.loads(line)
                mes = f"[CQ:image,file={result_dict['图片']}]\n{result_dict['标题']}\n原价:{result_dict['原价']}\n链接:{result_dict['链接']}\n"
                data = {
                "type": "node",
                "data": {
                    "name": "sbeam机器人",
                    "uin": "2854196310",
                    "content":mes
                        }
                    }
                mes_list.append(data)
        await bot.send(ev, "正在生成合并消息，请稍等片刻！")
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list, at_sender=True)
    except:
        pass

#后接格式：页数(阿拉伯数字) 标签1 标签2，例：st搜标签1 动作 射击
@sv.on_prefix(('st搜标签','St搜标签','ST搜标签'))
async def search_tag(bot, ev):
    model = ev.message.extract_plain_text().strip().split(" ")
    url = url_decide(model, int(model[0]))
    if url[1] == "":
        await bot.send(ev, "没有匹配到有效标签")
        pass
    else:
        await bot.send(ev, "正在搜索...")
        try:
            crawler(url[0])
        except:
            await bot.send(ev, "哦吼，出错了，请检查运行日志或者稍后再试")
        mes_list = []
        with open(FILE_NAME(url[0]), "r", encoding="utf-8")as f:
            for line in f.readlines():
                result_dict = json.loads(line)
                mes = f"[CQ:image,file={result_dict['图片']}]\n{result_dict['标题']}\n原价:{result_dict['原价']}\n链接:{result_dict['链接']}\n"
                data = {
                "type": "node",
                "data": {
                    "name": "sbeam机器人",
                    "uin": "2854196310",
                    "content":mes
                        }
                    }
                mes_list.append(data)
        await bot.send(ev, f"标签{url[1].strip(',')}搜索结果如下:")
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list, at_sender=True)

#后接游戏名，例：st搜游戏泰坦陨落
@sv.on_prefix(('st搜游戏','St搜游戏','ST搜游戏'))
async def search_term(bot, ev):
    term = ev.message.extract_plain_text().strip()
    url_term = "https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_151_7&infinite=1&term=" + term
    try:
        crawler(url_term)
    except:
        await bot.send(ev, "哦吼，出错了，请检查运行日志或者稍后再试")
    mes_list = []
    try:
        with open(FILE_NAME(url_term), "r", encoding="utf-8")as f:
            for line in f.readlines():
                result_dict = json.loads(line)
                mes = f"[CQ:image,file={result_dict['图片']}]\n{result_dict['标题']}\n原价:{result_dict['原价']}\n链接:{result_dict['链接']}\n"
                data = {
                "type": "node",
                "data": {
                    "name": "sbeam机器人",
                    "uin": "2854196310",
                    "content":mes
                        }
                    }
                mes_list.append(data)
        await bot.send(ev, f"游戏{term}搜索结果如下:")
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list, at_sender=True)
    except:
        await bot.send(ev, "无搜索结果")


@sv.scheduled_job('cron', hour='*')
async def cycle():
    try:
        crawler(url_new)
        crawler(url_specials)
    except:
        pass
    

#每半小时清理缓存的搜索结果
@sv.scheduled_job('cron', hour='*', minute='30')
async def cycle():
    try:
        for files in os.walk(FILE_PATH):
            for i in files[2]:
                if "search" in i:
                    name = os.path.join(FILE_PATH, i)
                    os.remove(name)
    except:
        pass