# Breadbot

## Overview
Breadbot is a fully open source, simple and powerful chatbot.
* Easy to deploy
* Fast response
* More than 1000,000 corpus
* No database
* Based on Python3
* Support WeChat

Visit the homepage [Breadbot.Fun](http://breadbot.fun) for more info.

## Have a try
* Download WeChat on your phone
* Login WeChat and scan the QR code
* ![QR](QR.jpg)
* Talk to Breadbot

## Install
Breadbot works on Linux. Of cause u can let it work on other OS by modify the source code.
* Download:
  * `git clone https://github.com/ideamark/breadbot`
* Install:
  * First, make sure you have installed python3 and python3-pip.
  * run setup command: `python3 setup.py install`
* Uninstall:
  * `python3 setup.py uninstall`
* Clean (not uninstall):
  * `python3 setup.py clean`

## Corpus
* All the corpus of Breadbot is on [Breadbot.Fun](http://breadbot.fun), which is a website and also a git repo.
* The repo will be downloaded automatically when you setup Breadbot by `python3 setup.py install`.

## Config
* Just watch the only single config file: [bread.cfg](etc/bread.cfg)

## Console
* Type command `breadbot` to launch the local console.
* Then u can test Breadbot. Type `help` for more info.

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
