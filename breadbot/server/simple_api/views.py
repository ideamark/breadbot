from rest_framework.response import Response
from rest_framework.views import APIView

from breadbot import core


db = core.common.get_db()

class simpleAPI(APIView):
    
    def post(self, request):
        user = request.user.get_username()
        qus = request.data.get('question', '')
        ans = core.chat.Chat(db).response(user, qus)
        data = {
            'user': user,
            'answer': ans
        }
        return Response(data)