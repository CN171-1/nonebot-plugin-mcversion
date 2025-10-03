from nonebot.plugin import PluginMetadata
from pydantic import BaseModel

__plugin_meta__ = PluginMetadata(
    name="MC版本更新检测",
    description="一个用于检测MC最新版本的插件",
    usage="使用 mcver 以获取最新版本号",
    type="application",
    homepage="https://github.com/CN171-1/nonebot_plugin_mcversion",
    supported_adapters={"~onebot.v11"},
)

# 导入必要的库
import os
import httpx
from datetime import datetime
from nonebot import on_command, get_bots, require, logger, get_plugin_config
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.message import Message

# 定义配置模型
class MCVersionConfig(BaseModel):
    mcver_proxies: str = None  # 代理设置
    mcver_group_id: list[int | str] = []
    """MC版本更新推送的群组ID列表"""

# 获取配置
config = get_plugin_config(MCVersionConfig)
mcver_group_id = config.mcver_group_id
proixes = config.mcver_proxies

# 定义命令“mcver”
mcver = on_command('mcver', aliases={'mcversion', 'MC版本'}, priority=50)

# 处理命令“mcver”
@mcver.handle()
async def mcver_handle():
    # 获取Minecraft版本信息
    async with httpx.AsyncClient(proxies=proixes) as client:
        response = await client.get("http://launchermeta.mojang.com/mc/game/version_manifest.json")
    data = response.json()
    latest_release = data['latest']['release']
    latest_snapshot = data['latest']['snapshot']
    # 发送消息
    await mcver.finish(message=Message(f'最新正式版：{latest_release}\n最新快照版：{latest_snapshot}'))

# 获取nonebot的调度器
scheduler = require('nonebot_plugin_apscheduler').scheduler

# 定义异步函数，用于检查Minecraft更新
async def check_mc_update(bot: Bot):
    # 获取Minecraft版本信息
    async with httpx.AsyncClient(proxies=proixes) as client:
        response = await client.get("http://launchermeta.mojang.com/mc/game/version_manifest.json")
    data = response.json()
    version = data["versions"][0]
    if not os.path.exists('data/latest_version.txt'):
        with open('data/latest_version.txt', 'w') as f:
            f.write(version["id"])
    with open('data/latest_version.txt', 'r') as f:
        old_version = f.read()
    if version["id"] != old_version:
        release_time = version["releaseTime"]
        release_time = datetime.strptime(release_time, '%Y-%m-%dT%H:%M:%S%z')
        release_time = release_time.replace(hour=release_time.hour + 8)
        release_time = release_time.strftime('%Y-%m-%dT%H:%M:%S+08')
        
        # 检查是否配置了群组ID
        if mcver_group_id:
            for group_id in mcver_group_id:
                try:
                    await bot.send_group_msg(
                        group_id=int(group_id),
                        message=Message(f'发现MC更新：{version["id"]} ({version["type"]})\n时间：{release_time}')
                    )
                except Exception as e:
                    logger.error(f"向群组 {group_id} 发送MC更新消息失败: {e}")
            logger.success("已发现并成功推送MC版本更新信息")
        else:
            logger.warning("未配置MC版本更新推送群组，跳过推送")
            
        with open('data/latest_version.txt', 'w') as f:
            f.write(version["id"])

# 定义定时任务，每分钟检查一次Minecraft更新
@scheduler.scheduled_job('interval', minutes=1)
async def mc_update_check():
    bots = get_bots()
    bot = None  # 初始化bot为None
    if bots:
        bot = list(bots.values())[0]  # 获取第一个机器人实例
    if bot:
        await check_mc_update(bot)
    else:
        logger.error("未找到机器人实例,请确保NoneBot已与QQ服务器建立连接")
