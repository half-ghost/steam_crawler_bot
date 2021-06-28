# steam_crawler_bot
这是一个基于HoshinoBot的插件，目前所拥有的功能有：
- **查询今日特惠以及今日新品信息**
> 命令：今日特惠 or 今日新品
- **根据输入的标签查询结果，所有steam标签详见tag.json**
> 命令：st搜标签 后接格式：页数(阿拉伯数字) 标签1 标签2，例：st搜标签1 动作 射击
- **根据输入的游戏名字查询结果**
> 命令：st搜游戏 后接游戏名字

**使用方法：**

在HoshinoBot的modules文件夹下新建一个steam_crawler_bot文件夹，并将本项目的文件复制进去，然后在hoshino/config/__bot__.py中的MODULES_ON中添加'steam_crawler_bot'

HoshinoBot的部署详见[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
