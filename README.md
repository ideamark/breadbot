# Breadbot

## Overview
* Breadbot is a simple and powerful chatbot
  * Easy to deploy
  * More than 1000,000 corpus
  * Fast response
  * Based on Python3
  * Support WeChat

## Setup
* Download
  * git clone https://github.com/ideamark/breadbot
* Install
  * Make sure you have installed python3, python3-pip and mongodb
  * python3 setup.py install
  * The setup will download corpus from https://github.com/ideamark/ideamark.github.io
* Uninstall
  * python3 setup.py uninstall
* Clean (not uninstall)
  * python3 setup.py clean
* Import all corpus
  * The setup will only import basic corpus. If you want to import all corpus, just type "breadbot import". It may take a long time to finish importing.

## Config
* Just watch the only single config file: [bread.cfg](etc/bread.cfg)

## Console
* Type command "breadbot" to launch the local console.
* Then u can test Bread, or run commands on this console, type "help" for more info.

## Super user mode
* Super user mode is set for developers.
* The local console is default set as super user.
* If your ID is in bread.cfg super user list, u will get the super user functions below:
  * Type "help": Simple & quick help.
  * Type "readme": Display README file.
  * Type "d xxx": Search knowledge base and baidu.
  * Type "w xxx": Search wikipedia.
  * Type "s xxx": Search google translator
  * Type "t que: ans": Teach a dialogue and save it in data/teach.yml

## Connect to WeChat
* Write your token and IP on /etc/bread.cfg, then run command "breadbot start", it will soon connect to WeChat Official Account (https://mp.weixin.qq.com) and u can chat with Bread on WeChat.

## Seek more
* Author: Mark Young
* Email: ideamark@qq.com
