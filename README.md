# steam_crawler_bot
这是一个基于HoshinoBot的steam爬虫插件，可以根据命令来爬取相关信息，并以合并消息的形式发送。目前所拥有的功能有：
- **查询今日特惠以及今日新品信息（默认返回50条）**
> 命令：今日特惠 or 今日新品

![](https://z3.ax1x.com/2021/06/29/RUbNOP.jpg)
- **根据输入的标签查询结果，所有steam标签详见tag.json（默认返回50条，标签需要全匹配,会过滤没匹配到的标签）**
> 命令：st搜标签 后接格式：页数(阿拉伯数字) 标签1 标签2，例：st搜标签1 动作 射击

![](https://z3.ax1x.com/2021/06/29/RUbO0K.jpg)
- **根据输入的游戏名字查询结果（能搜到多少条游戏信息就返回多少条）**
> 命令：st搜游戏 后接游戏名字

![](https://z3.ax1x.com/2021/06/29/RUqA78.jpg)

**使用方法：**

在HoshinoBot的modules文件夹下新建一个steam_crawler_bot文件夹，并将本项目的文件复制进去，然后在hoshino/config/__bot__.py中的MODULES_ON中添加'steam_crawler_bot'

HoshinoBot的部署详见[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)

# 计划

或许会加入更多奇奇怪怪的功能，敬请期待
