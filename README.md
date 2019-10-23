# Breadbot

## Overview
Breadbot is a lightweight chatbot with powerful AI inside.
* Opened both code and corpus
* More than 1000,000 corpus
* Very easy to deploy & use
* Fast response
* Support WeChat

Visit the homepage [Breadbot.Fun](http://breadbot.fun) for more info.

## Have a try
* Download WeChat on your phone
* Login WeChat and scan the QR code
* ![QR](QR.jpg)
* Talk to Breadbot

## Quick Install
Breadbot works on Linux. Of cause u can let it work on other OS by modify the source code.
* Download:
  * `git clone https://github.com/ideamark/breadbot`
* Install:
  * First, make sure you have installed python3, python3-pip, python3-dev, gcc, redis-server.
  * run setup command: `python3 setup.py install`
  * The corpus will be downloaded during installation.
* Uninstall:
  * `python3 setup.py uninstall`
* Clean (not uninstall):
  * `python3 setup.py clean`

## Let us start
1. Type `redis-server` to launch Redis on port 6379.
2. Type `breadbot` to launch the local console.
3. Type `import` to import corpus data.
4. Then u can test Breadbot. Type `help` for more info.

## Corpus
* All the corpus of Breadbot is on [Breadbot.Fun](http://breadbot.fun), which is a website and also a git repo.
* The repo will be downloaded automatically when you setup Breadbot by `python3 setup.py install`.

## Config
* Just watch the only single config file: [bread.cfg](etc/bread.cfg)

## Super user mode
* Super user mode is set for developers.
* The local console is default set as super user.
* If your WeChat ID is in [bread.cfg](etc/bread.cfg) super user list, u will get the super user functions.

## Import to your project
* Need root permission.
```python
from breadbot.core import response
response('localuser', 'hello')
```

## Connect to WeChat
* Config your WeChat public platform account on [mp.weixin.qq.com](https://mp.weixin.qq.com). Create the Token and enter your server URL.
* Then back to local server. Run the command `breadbot start` to launch the server. Enter your Token and server IP.
* After that, Breadbot will connect to WeChat public platform and u can chat to it on WeChat.

## Seek more
* Author: Mark Young (IdeaMark)
* Email: ideamark@qq.com
