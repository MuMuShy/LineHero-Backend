from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.decorators import method_decorator
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from line_hero.settings import LINE_BOT_API,LINE_HANDLER
from chatbot.models import User

@method_decorator(csrf_exempt, name='dispatch')
class LineBotCallback(View):
    def post(self, request, *args, **kwargs):
        # 获取 X-Line-Signature header 值
        signature = request.headers['X-Line-Signature']

        # 获取请求体内容
        body = request.body.decode('utf-8')

        try:
            # 调用处理函数处理请求
            LINE_HANDLER.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)

        return HttpResponse(status=200)
# 定义LINE Bot的消息处理函数
@LINE_HANDLER.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    print(event.source.user_id)
    line_user_id =event.source.user_id
    profile = LINE_BOT_API.get_profile(line_user_id)
    user_name = profile.display_name

    existing_user = User.objects.filter(line_user_id=line_user_id).first()

    if existing_user:
        # 用户已存在，可以更新用户信息或执行其他操作
        existing_user.name = user_name
        existing_user.save()
        response_message = "歡迎回來 冒險者" + user_name
    else:
        # 用户不存在，创建新的User对象并保存到数据库
        user = User(line_user_id=line_user_id, name=user_name)
        user.save()
        # 在这里添加你的消息处理逻辑
        response_message = "歡迎加入 冒險者" + user_name
    
    # 处理收到的文本消息
    text_message = event.message.text

    

    # 发送回复消息
    LINE_BOT_API.reply_message(
        event.reply_token,
        TextSendMessage(text=response_message)
    )