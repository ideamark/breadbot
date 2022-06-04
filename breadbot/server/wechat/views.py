from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.template import loader, Context
import hashlib
import time
from xml.etree import ElementTree as ET

from breadbot import core


db = core.common.get_db()


class WeChat(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChat, self).dispatch(*args, **kwargs)

    def get(self, request):
        token = core.common.Cfg().get('wechat', 'token')
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
        str_xml = ET.fromstring(request.body)
        from_user = str_xml.find('FromUserName').text
        to_user = str_xml.find('ToUserName').text
        cur_time = str(int(time.time()))
        msg_type = str_xml.find('MsgType').text
        content = '...'
        if msg_type == 'text':
            content = str_xml.find('Content').text
            if '[Unsupported Message]' in content:
                res = 'Error: unknow message'
            else:
                res = core.chat.Chat(db).response(from_user, content)
        else:
            res = "Sorry, I can't chat by %s" % msg_type
        template = loader.get_template('wechat/text_message_template.xml')
        context = {'toUser': from_user,
                   'fromUser': to_user,
                   'currentTtime': cur_time,
                   'content': res}
        context_xml = template.render(context)
        log_str = '\nUser:   %s\nAsk:    %s\nAnswer: %s\n' % \
                  (from_user, content, res)
        core.common.ChatLog().write(log_str)
        return HttpResponse(context_xml)
