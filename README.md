# Breadbot

## Overview
* Breadbot is a simple and powerful chatbot
  * Easy to deploy
  * More than 1000,000 corpus
  * Fast response
  * No database
  * Based on Python3
  * Support WeChat

## Have a try
* Download WeChat on your phone
* Login WeChat and scan the QR code
  * ![QR](QR.jpg)
* Talk to Breadbot

## Install
* You can also download the source code to build your own Breadbot.
* Note
  * Breadbot only works on Linux. Also u can let it work on other OS by modify the source code.
* Download
  * git clone https://github.com/ideamark/breadbot
* Install
  * First, make sure you have installed python3 and python3-pip
  * python3 setup.py install
  * The setup will download corpus from https://github.com/ideamark/ideamark.github.io
* Uninstall
  * python3 setup.py uninstall
* Clean (not uninstall)
  * python3 setup.py clean

## Config
* Just watch the only single config file: [bread.cfg](etc/bread.cfg)

## Console
* Type command "breadbot" to launch the local console.
* Then u can test Bread, or run commands on this console, type "help" for more info.

## Super user mode
* Super user mode is set for developers.
* The local console is default set as super user.
* If your ID is in bread.cfg super user list, u will get the super user functions.

## Connect to WeChat
* Config your WeChat public platform account on https://mp.weixin.qq.com, create the token and enter your url.
* Run the command "breadbot start", enter your token and ip.
* After that, Breadbot will connect to WeChat public platform and u can chat to it on WeChat.

## Seek more
* Author: Mark Young
* Email: ideamark@qq.com
