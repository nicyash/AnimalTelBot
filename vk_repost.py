import vk_api
import json
import requests

from config import VK_TOKEN

session = vk_api.VkApi(token=VK_TOKEN)
vk = session.get_api()


def repost_vk(message):

    vk.wall.post(message=message)
