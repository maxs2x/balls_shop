import vk_api
import requests
from vk_api.utils import get_random_id


vk_session = vk_api.VkApi(token='f46017229bcc5d6aea3da1b606ae40529e90d64db4da4601158016779830a197054e97eea6ac1f9975f96')
vk = vk_session.get_api()

def send_order(text):
    random_id = vk_api.utils.get_random_id()
    vk.messages.send( #Отправляем сообщение
                    user_id=int(10883803),
                    message=text,
                    random_id=random_id
		        )


# Строка для получения юзер ид
#if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#    print('id{}: "{}"'.format(event.user_id, event.text), end=' ')