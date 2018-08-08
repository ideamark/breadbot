# 小面包

## 概览
小面包（Breadbot）是一款功能强大，简单易部署的聊天AI.
* 一键部署
* 快速响应
* 开放百万级语料
* 免数据库
* 基于 Python3
* 支持微信对接

小面包的愿景是挖掘隐性知识的价值，请看我们的[主页](https://ideamark.github.io)。

## 试一试
* 微信扫描下方二维码开始和小面包聊天！
* ![QR](QR.jpg)

## 安装
小面包工作于 Linux，当然，你也可以通过修改代码使其工作于 Windows.
* 下载
  * `git clone https://gitee.com/ideamark/breadbot`
* 安装
  * 首先，确保你已经安装了 python3 和 python3-pip
  * 执行安装命令：`python3 setup.py install`
  * 安装过程会自动从 ideamark.github.io 下载语料。
* 卸载
  * `python3 setup.py uninstall`
* 清理 (不是卸载)
  * `python3 setup.py clean`

## 语料
* 小面包的全部语料都在 [ideamark.github.io](https://ideamark.github.io) 上，这是一个网站，同时也是个 Git 仓库。
* 当你运行安装命令 `python3 setup.py install` 的时候，这些语料会被自动下载到本地。
* 当然你也可以手动下载：`git clone https://github.com/ideamark/ideamark.github.io`

## 配置
* 只需阅读唯一的配置文件 [bread.cfg](etc/bread.cfg) 即可一目了然。

## 终端
* 输入命令 `breadbot` 可以启动小面包的终端。
* 然后你就可以测试小面包了，输入`help` 查看更多信息。

## 超级用户
* 超级用户是为了方便开发者设置的。
* 本地终端已默认设置为超级用户。
* 如果你的微信 ID 在 [bread.cfg](etc/bread.cfg) 的超级用户列表里，你就能使用超级用户相关功能。

## 导入到你的工程
* 需要 root 权限
> from breadbot.core import response
> response('localuser', 'hello')

## 连接微信
* 登录微信公众平台 [mp.weixin.qq.com](https://mp.weixin.qq.com)，创建 Token 并输入你的服务器 URL.
* 回到本地服务器，运行命令 `breadbot start` 启动服务，输入你的 Token 和服务器 IP.
* 然后，小面包就会连接到微信公众平台，你就可以通过微信和小面包聊天了。

## 更多
* 作者：Mark Young (IdeaMark)
* 邮箱：ideamark@qq.com
