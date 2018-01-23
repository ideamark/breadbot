from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.template import loader, Context
import hashlib
import time
from xml.etree import ElementTree as ET

from breadbot import core


class WeChat(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChat, self).dispatch(*args, **kwargs)

    def get(self, request):
        token = core.misc.cfg().get('token')
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        list = [token, timestamp, nonce]
        list.sort()
        hashcode = ''.join([s for s in list])
        hashcode = hashlib.sha1(hashcode.encode('ascii')).hexdigest()
        if hashcode == signature:
            return HttpResponse(echostr)

    def post(self, request):
        strXml = ET.fromstring(request.body)
        fromUser = strXml.find('FromUserName').text
        toUser = strXml.find('ToUserName').text
        currentTime = str(int(time.time()))
        msgType = strXml.find('MsgType').text
        content = '...'
        sorry = 'Sorry, I only support text chatting'
        if msgType == 'text':
            content = strXml.find('Content').text
            if '[Unsupported Message]' in content:
                res = sorry
            else:
                res = core.chat().response(fromUser, content)
        else:
            res = sorry
        template = loader.get_template('wechat/text_message_template.xml')
        context = Context({'toUser': fromUser,
                           'fromUser': toUser,
                           'currentTime': currentTime,
                           'content': res})
        contextXml = template.render(context)
        logStr = '\nUser:   %s\nAsk:    %s\nAnswer: %s\n' % \
                 (fromUser, content, res)
        core.misc.log().write(logStr)
        return HttpResponse(contextXml)
