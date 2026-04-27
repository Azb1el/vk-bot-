import  vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import config  as cfg

vk_session = vk_api.VkApi(token=cfg.VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print(event.text)