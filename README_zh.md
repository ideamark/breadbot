# 小面包

## 概览
小面包（Breadbot）是一款还在实验阶段的新式聊天机器人框架, 旨在大大简化聊天机器人的开发难度.

* 同时开放源码和海量语料资源
* Wiki 式语料组织, 更易阅读和编写
* 极简设计风格, 一键部署, 快速响应

访问主页 [Breadbot.Fun](http://breadbot.fun) 获取更多信息。

## 试一试
* 微信扫描下方二维码开始和小面包聊天！
* ![QR](QR.jpg)

## 一键安装
小面包工作于 Linux，当然，你也可以通过修改代码使其工作于 Windows.
* 下载：
  * `git clone https://gitee.com/ideamark/breadbot`
* 安装：
  * 首先，确保你已经安装了 python3, python3-pip, python3-dev, gcc, redis-server.
  * 执行安装命令：`python3 setup.py install`
  * 安装过程中会下载语料
* 卸载：
  * `python3 setup.py uninstall`
* 清理 (不是卸载)：
  * `python3 setup.py clean`

## 快速启动
1. 输入命令 `redis-server` 在本地 6379 端口启动 Redis 数据库。
2. 输入命令 `breadbot` 启动小面包终端。
3. 输入命令 `import` 导入语料数据。
4. 然后你就可以和小面包对话了，输入`help` 可以查看更多信息。

## 语料
* 小面包的全部语料都在 [Breadbot.Fun](http://breadbot.fun) 上，这是一个网站，同时也是个 Git 仓库。
* 当你运行安装命令 `python3 setup.py install` 的时候，这些语料会被自动下载到本地。

## 配置
* 只需阅读唯一的配置文件 [bread.cfg](etc/bread.cfg) 即可一目了然。

## 超级用户
* 超级用户是为了方便开发者设置的。
* 本地终端已默认设置为超级用户。
* 如果你的微信 ID 在 [bread.cfg](etc/bread.cfg) 的超级用户列表里，你就能使用超级用户相关功能。

## 导入到你的工程
* 需要 root 权限
```python
from breadbot.core import response
response('localuser', 'hello')
```

## 连接微信
* 登录微信公众平台 [mp.weixin.qq.com](https://mp.weixin.qq.com)，创建 Token 并输入你的服务器 URL.
* 回到本地服务器，运行命令 `breadbot start` 启动服务，输入你的 Token 和服务器 IP.
* 然后，小面包就会连接到微信公众平台，你就可以通过微信和小面包聊天了。

## 更多
* 作者：Mark Yang (IdeaMark)
* 邮箱：ideamark@qq.com
* 欢迎加入开发, 直接联系作者邮箱
* 欢迎捐赠，支持中国开源事业
