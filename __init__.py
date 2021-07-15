help = '''
本插件有如下指令：
1.[今日特惠 or 今日新品]：爬取steam的特惠或新品页的数据并发送合并消息
2.[st搜标签]：后接格式为页数(阿拉伯数字) 标签a 标签b，例：st搜标签1 射击 多人，
即搜索射击和多人的标签的第一页，由于steam一页有50个数据，故一次返回50条消息
3.[st搜游戏]：后接游戏名称，只可同时搜索一个游戏，返回的数据为输入内容的真实搜索结果，
所以如果想要搜索的游戏是英文名，而用户搜索的是该游戏的译名，则可能搜到的不是想要的结果
4.[小黑盒查询]：从小黑盒官网爬取数据，包含了爬取到的游戏是否处于史低价以及是否新史低的信息
[小黑盒查询页]：后接页数(阿拉伯数字)由于小黑盒官网数据最多可以一次性抓取到30条结果，
故设置了这个命令，可以按照页数来爬取

*以上除了小黑盒的数据来自于小黑盒官网外，其他抓取内容数据均来自steam官网
'''.strip()

from hoshino import Service
from .steam_crawler_bot import crawler,url_decide,hey_box

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
