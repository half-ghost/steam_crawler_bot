help = f'''
本插件有如下指令：
1.[今日特惠 or 今日新品]：爬取steam的特惠或新品页的数据并发送合并消息
2.[st搜标签]：后接格式为页数(阿拉伯数字) 标签a 标签b，例：st搜标签1 射击 多人，\
即搜索射击和多人的标签的第一页，由于steam一页有50个数据，故一次返回50条消息
3.[st搜游戏 or 小黑盒搜]：后接游戏名称，只可同时搜索一个游戏，返回的数据为输入内容的真实搜索结果，\
某些有中译名字的游戏在steam上的原名可能为英文名，所以如果搜索的是该游戏的译名，则可能搜到的不是想要的结果。\
小黑盒搜游戏可以使用中文译名，但请尽量不要使用简写（如怪物猎人简写为怪猎，是搜不到的）
4.[小黑盒查询]：从小黑盒官网爬取数据，包含了爬取到的游戏是否处于史低价以及是否新史低的信息
[小黑盒查询页]：后接页数(阿拉伯数字)由于小黑盒官网数据最多可以一次性抓取到30条结果，\
故设置了这个命令，可以按照页数来爬取
5.[喜加一资讯]：后接想要获取的资讯条数(阿拉伯数字)
6.[开启 or 关闭喜加一提醒]：开启或关闭在本群的喜加一提醒服务

*以上除了小黑盒的数据来自于小黑盒官网外，其他抓取内容数据均来自steam官网，喜加一数据来源于IT之家
'''.strip()

from hoshino import Service,get_bot,priv
from .steam_crawler_bot import crawler,url_decide,hey_box,hey_box_search
from .xjy import xjy_compare,xjy_result
import os
import json

FILE_PATH = os.path.join(os.path.dirname(__file__))
sv = Service("stbot")
url_new = "https://store.steampowered.com/search/results/?l=schinese&query&sort_by=Released_DESC&category1=998&os=win&infinite=1&start=0&count=50"
url_specials = "https://store.steampowered.com/search/results/?l=schinese&query&sort_by=_ASC&category1=998&specials=1&os=win&filter=topsellers&start=0&count=50"


# 匹配关键词发送相关信息，例：今日特惠，发送今日特惠信息，今日新品则发送新品信息
@sv.on_prefix('今日')
async def Gameinfo(bot, ev):
    model = ev.message.extract_plain_text().strip()
    if model == "新品":
        try:
            mes_list = crawler(url_new)
            await bot.send(ev, "正在生成合并消息，请稍等片刻！", at_sender=True)
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
        except Exception as e:
            sv.logger.error(f"Error:{e}")
            await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")
    elif model == "特惠":
        try:
            mes_list = crawler(url_specials)
            await bot.send(ev, "正在生成合并消息，请稍等片刻！", at_sender=True)
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
        except Exception as e:
            sv.logger.error(f"Error:{e}")
            await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")

# 后接格式：页数(阿拉伯数字) 标签1 标签2，例：st搜标签1 动作 射击
@sv.on_prefix(('st搜标签','St搜标签','ST搜标签'))
async def search_tag(bot, ev):
    model = ev.message.extract_plain_text().strip().split(" ")
    url = url_decide(model, int(model[0]))
    if url[1] == "":
        await bot.send(ev, "没有匹配到有效标签")
        pass
    else:
        try:
            mes_list = crawler(url[0])
            await bot.send(ev, "正在搜索并生成合并消息中，请稍等片刻！", at_sender=True)
            await bot.send(ev, f"标签{url[1].strip(',')}搜索结果如下:")
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
        except Exception as e:
            sv.logger.error(f"Error:{e}")
            await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")
        
# 后接游戏名，例：st搜游戏美少女万华镜
@sv.on_prefix(('st搜游戏','St搜游戏','ST搜游戏'))
async def search_term(bot, ev):
    term = ev.message.extract_plain_text().strip()
    url_term = "https://store.steampowered.com/search/results/?l=schinese&query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_151_7&infinite=1&term=" + term
    try:
        mes_list =crawler(url_term)
        if len(mes_list) == 0:
            await bot.send(ev, "无搜索结果")
        else:
            await bot.send(ev, f"游戏{term}搜索结果如下:", at_sender=True)
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
    except Exception as e:
        sv.logger.error(f"Error:{e}")
        await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")

# 此为小黑盒查询默认情况，默认抓取第一页(每页30条信息)
@sv.on_fullmatch('小黑盒查询')
async def heybox(bot, ev):
    try:
        mes_list = hey_box(1)
        await bot.send(ev, "正在搜索并生成合并消息中，请稍等片刻！", at_sender=True)
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
    except Exception as e:
        sv.logger.error(f"Error:{e}")
        await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")

# 后接页数(阿拉伯数字)，例：小黑盒查询页1
@sv.on_prefix('小黑盒查询页')
async def heybox(bot, ev):
    page = int(ev.message.extract_plain_text().strip())
    try:
        mes_list = hey_box(page)
        await bot.send(ev, "正在搜索并生成合并消息中，请稍等片刻！", at_sender=True)
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
    except Exception as e:
        sv.logger.error(f"Error:{e}")
        await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")

# 后接游戏名称
@sv.on_prefix('小黑盒搜')
async def heybox_search(bot, ev):
    game = ev.message.extract_plain_text().strip()
    try:
        mes_list = hey_box_search(game)
        if len(mes_list) != 1:
            await bot.send(ev, "正在搜索并生成合并消息中，请稍等片刻！", at_sender=True)
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)
        else:
            await bot.send(ev, "无搜索结果")
    except Exception as e:
        sv.logger.error(f"Error:{e}")
        await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")

# 后接想要看的资讯条数（阿拉伯数字）
@sv.on_prefix('喜加一资讯')
async def xjy_info(bot, ev):
    if os.path.exists(os.path.join(FILE_PATH, "xjy_result.txt")) == False:
        try:
            xjy_compare()
        except Exception as e:
            sv.logger.error(f"Error:{e}")
            await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")
    num = ev.message.extract_plain_text().strip()
    state1 = xjy_result("Query", int(num))
    mes_list = []
    if "error" in state1:
        sv.logger.error(state1)
        await bot.send(ev, "哦吼，出错了，请检查主机网络情况、查看运行日志或者再试一遍")
        pass
    else:
        if len(state1) <= 2:
            for i in state1:
                await bot.send(ev, message = i)
        else:
            for i in state1:
                data = {
                    "type": "node",
                    "data": {
                        "name": "sbeam机器人",
                        "uin": "2854196310",
                        "content":i
                            }
                        }
                mes_list.append(data)
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=mes_list)

# 这部分直接抄了@H-K-Y(https://github.com/H-K-Y)大佬的原神插件里的一部分代码
group_list = []
def save_group_list():
    with open(os.path.join(FILE_PATH,'group_list.json'),'w',encoding='UTF-8') as f:
        json.dump(group_list,f,ensure_ascii=False)

# 检查group_list.json是否存在，没有创建空的
if not os.path.exists(os.path.join(FILE_PATH,'group_list.json')):
    save_group_list()

# 读取group_list.json的信息
with open(os.path.join(FILE_PATH,'group_list.json'),'r',encoding='UTF-8') as f:
    group_list = json.load(f)

# 喜加一提醒开关
@sv.on_fullmatch('开启喜加一提醒')
async def open_remind(bot , ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, "你没有权限这么做")
        return
    gid = str(ev.group_id)
    if not (gid in group_list):
        group_list.append(gid)
        save_group_list()
    await bot.send(ev, "喜加一提醒已开启，如有新喜加一信息则会推送")

@sv.on_fullmatch('关闭喜加一提醒')
async def off_remind(bot , ev):
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.send(ev, "你没有权限这么做")
        return
    gid = str(ev.group_id)
    if gid in group_list:
        group_list.remove(gid)
        save_group_list()
    await bot.send(ev, "喜加一提醒已关闭")

# 定时检查是否有新的喜加一信息
@sv.scheduled_job('cron', hour='*', minute = '*')
async def xjy_remind():
    bot = get_bot()
    url_list = xjy_compare()
    if "Server Error" in url_list:
        sv.logger.info("访问it之家出错，非致命错误，可忽略")
    elif "error" in url_list:
        sv.logger.error(url_list)
    elif len(url_list) != 0:
        mes = xjy_result("Default",url_list)
        for gid in group_list:
            await bot.send_group_msg(group_id=int(gid),message="侦测到在途的喜加一信息，即将进行推送...")
            for i in mes:
                await bot.send_group_msg(group_id=int(gid),message=i)
    else:
        sv.logger.info("无新喜加一信息")

@sv.on_fullmatch(('st机器人帮助','St机器人帮助','ST机器人帮助'))
async def bot_help(bot, ev):
    await bot.send(ev, help)
