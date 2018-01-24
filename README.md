# Bread Bot

## Overview
* Bread Bot is a pure-Python, pure-text chatterbot. The aim is to build a fast speed, short text message QA system.
  * Why Python: For platform independence and fast development.
  * Why text only: Text can express anything, easily to be processed, fast to be translated. That's why we only use text message for Bread Bot.

## Setup
* Install
  * Make sure you have installed python3, python3-pip and mongodb
  * sudo python3 setup.py install
* Uninstall
  * sudo python3 setup.py uninstall
* Clean (not uninstall)
  * sudo python3 setup.py clean

## How to use
* Run command "breadbot"
* Then u can talk with Bread
  * Only English chatting.
  * If return message is too long, type "n" turn to next page.

## Super user mode
* Super user mode is set for developers.
* If your ID is in bread.cfg super user list, u will get the functions below:
  * Type "help": Simple & quick help.
  * Type "readme": Display this web page.
  * Type "d xxx": Search knowledge base and baidu.
  * Type "w xxx": Search wikipedia.
  * Type "s xxx": Search dictionary(Need install sdcv first).
  * Type "t que;ans": Teach dialogues(Use ";" to split question and answer)

## Connect to WeChat
* Write your token and ip on /etc/bread.cfg, then run command "breadbot start", it will soon connect to WeChat Official Account (https://mp.weixin.qq.com) and start working.

## Seek more
* Author: Mark Young
* Email: ideamark@qq.com
