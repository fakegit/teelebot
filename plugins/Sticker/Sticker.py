from teelebot import Bot
import requests
from threading import Timer

bot = Bot()

def Sticker(message):
    chat_id = message["chat"]["id"]
    message_id = message["message_id"]
    text = message["text"]
    prefix = "getsticker"

    if text[1:len(prefix)+1] == prefix:
        if "reply_to_message" in message.keys():
            if "sticker" in message["reply_to_message"].keys():
                file_id = message["reply_to_message"]["sticker"]["file_id"]
                file_dl_path = bot.getFileDownloadPath(file_id=file_id)
                req = requests.get(url=file_dl_path)
                if type(req.content) == bytes:
                    photo = req.content
                else:
                    photo = file_dl_path
                status = bot.sendChatAction(chat_id, "typing")
                status = bot.sendPhoto(chat_id=chat_id, photo=photo, caption="本消息不久将被销毁，请尽快保存。" , reply_to_message_id=message_id)
                timer = Timer(30, timer_func, args=[chat_id, status["message_id"]])
                timer.start()
            else:
                status = bot.sendChatAction(chat_id, "typing")
                status = bot.sendPhoto(chat_id=chat_id, text="您未指定要获取的贴纸!", parse_mode="text", reply_to_message_id=message_id)
                timer = Timer(15, timer_func, args=[chat_id, status["message_id"]])
                timer.start()
        else:
            status = bot.sendChatAction(chat_id, "typing")
            status = bot.sendMessage(chat_id=chat_id, text="您未指定要获取的贴纸!", parse_mode="text", reply_to_message_id=message_id)
            timer = Timer(15, timer_func, args=[chat_id, status["message_id"]])
            timer.start()

def timer_func(chat_id, message_id):
    status = bot.deleteMessage(chat_id=chat_id, message_id=message_id)