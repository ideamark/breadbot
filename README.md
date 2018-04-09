# Bread Bot

## Overview
* Bread Bot is a pure-Python, pure-text chatbot. The aim is to build a fast speed, short text message chat AI.
  * Why Python: For platform independence and fast development.
  * Why text only: Text can express anything, easily to be processed, fast to be translated. That's why we only use text message for Bread Bot.

## Setup
* Install
  * Make sure you have installed python3, python3-pip and mongodb
  * python3 setup.py install
* Uninstall
  * python3 setup.py uninstall
* Clean (not uninstall)
  * python3 setup.py clean

## Local console
* Type command "breadbot" to launch the local console.
* Then u can test Bread, or run commands on this console, type "help" for more info.

## Super user mode
* Super user mode is set for developers.
* The local console is default set as super user.
* If your ID is in bread.cfg super user list, u will get the super user functions below:
  * Type "help": Simple & quick help.
  * Type "readme": Display this web page.
  * Type "d xxx": Search knowledge base and baidu.
  * Type "w xxx": Search wikipedia.
  * Type "s xxx": Search dictionary(Need install sdcv first).
  * Type "t que;ans": Teach dialogues(Use ";" to split question and answer)

## Connect to WeChat
* Write your token and ip on /etc/bread.cfg, then run command "breadbot start", it will soon connect to WeChat Official Account (https://mp.weixin.qq.com) and u can chat with Bread on WeChat!

## More corpus
* The basic corpus is in the data folder
* There's more corpus on https://github.com/ideamark/breadbot_corpus

## Seek more
* Author: Mark Young
* Email: ideamark@qq.com
