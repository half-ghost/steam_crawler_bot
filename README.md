# steam_crawler_bot
这是一个基于HoshinoBot的steam爬虫插件，可以根据命令来爬取相关信息，并以合并消息的形式发送。目前所拥有的功能有：

注：**与steam相关的查询数据来源于steam官网，与小黑盒相关的查询数据来源于小黑盒官网，喜加一数据来源于it之家**

- **查询今日特惠以及今日新品信息（默认返回50条）**
> 命令：今日特惠 or 今日新品

<img src="https://z3.ax1x.com/2021/06/29/RdOwkV.jpg" width = "35%" height = "35%" align=center />

- **根据输入的标签查询结果，所有steam标签详见tag.json（默认返回50条，标签需要全匹配,会过滤没匹配到的标签）**
> 命令：st搜标签 后接格式：页数(阿拉伯数字) 标签a 标签b，(记得用空格隔开)例：st搜标签1 动作 射击

<img src="https://z3.ax1x.com/2021/06/29/RdOsl4.jpg" width = "35%" height = "35%" align=center />

- **根据输入的游戏名字查询结果（能搜到多少条游戏信息就返回多少条）**
> 命令：st搜游戏、小黑盒搜 后接游戏名字

<img src="https://z3.ax1x.com/2021/06/29/RdORTx.jpg" width = "35%" height = "35%" align=center />
<img src="https://z3.ax1x.com/2021/07/27/WIGfLF.jpg" width = "35%" height = "35%" align=center />

- **小黑盒数据查询，包含了爬取到的游戏是否处于史低以及是否新史低的信息**
> 命令：小黑盒查询/小黑盒查询页（后接阿拉伯数字）

<img src="https://z3.ax1x.com/2021/07/04/Rfrq7q.jpg" width = "35%" height = "35%" align=center />

- **喜加一信息获取以及推送服务**
> 命令：喜加一资讯（后接阿拉伯数字）

> 命令：开启 or 关闭喜加一提醒（需要群管理员或者机器人管理员权限）

<img src="https://z3.ax1x.com/2021/08/05/feTS54.png" width = "35%" height = "35%" align=center />

**更多详细请发送"st机器人帮助"获取**

**使用方法：**

在HoshinoBot的modules文件夹下新建一个steam_crawler_bot文件夹，并将本项目的文件复制进去，然后在hoshino/config/\_\_bot\_\_.py中的MODULES_ON中添加'steam_crawler_bot'

HoshinoBot的部署详见[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)

# 更新

2021.8.19 优化喜加一爬虫的数据处理

2021.8.5 新增喜加一信息推送及查询功能

2021.7.27 新增小黑盒搜游戏功能，可以返回在小黑盒搜到的游戏结果。在源自小黑盒的数据结果中新增了折扣比以及打折截止日期

<img src="https://z3.ax1x.com/2021/07/27/WIJfpt.jpg" width = "35%" height = "35%" align=center />

2021.7.15 修复小黑盒查询可能会报错的情况，抛弃原本文本缓存机制，精简代码（怎么这垃圾插件代码越写越少

2021.7.11 改善tag.json的数据结构，使其读取更方便快速。在来源自steam的搜索结果中新增了折扣比、用户评测以及热门用户自定义标签三项信息

<img src="https://z3.ax1x.com/2021/07/11/W9zAUO.jpg" width = "35%" height = "35%" align=center />

2021.7.7 有个定时任务似乎会造成hoshino程序卡死，先暂时删除该定时任务，后续再考虑解决方案

2021.7.4 新增了小黑盒数据爬取功能，优化了一些报错的提示，以及使代码规范化了一些

# 计划

或许会加入更多奇奇怪怪的功能，欢迎提交pr或issue来告诉我你们希望能加入什么功能
