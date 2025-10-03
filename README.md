# README
<!--
<div align="center">
  <img src="your_project_logo.png" alt="Logo" width="200">
</div>
-->
## 描述

该项目是一个使用 Python 编写的简单程序，用于获取 Minecraft 最新版本信息并定时检查更新，并在指定的群组内发送消息通知。

## 功能特点

- 获取最新的 Minecraft 版本信息
- 定时检查 Minecraft 是否有新版本
- 在指定群组内发送更新通知消息

## 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-mcversion

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-mcversion
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-mcversion
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-mcversion
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-mcversion
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-mcversion"]

</details>

## 使用

1. 使用 `mcver` , `mcversion` ,`MC版本` 来获取当前最新MC版本
2. 程序会每分钟自动检查 Minecraft 是否有新版本，若有则会在指定的群组内发送消息。

## 配置

在配置文件中必须进行以下设置：

- `mcver_group_id`：指定检查 Minecraft 更新后发送消息的群组 ID。
- `mcver_proixes`：指定使用的代理地址

例如：
```
mcver_group_id = [123456, 789012]
mcver_proxies = "http://127.0.0.1:7890"
```

## 鸣谢

- [nonebot-plugin-apscheduler](https://github.com/nonebot/plugin-apscheduler) - NoneBot 的定时任务插件

## 反馈

- 问题跟踪：[GitHub Issues](https://github.com/CN171-1/nonebot-plugin-mcversion/issues)
