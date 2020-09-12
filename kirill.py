import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from datetime import datetime, timezone, date,  timedelta
from threading import Timer
from threading import Thread
import typing
import re
import logging
import asyncio
import random
from time import gmtime, strftime
import threading
import json
from typing import Union
#import locale
#locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
import wikipedia
import urllib.request
from bs4 import BeautifulSoup





def info_msg_id(peer_id):
    history = vk.method('messages.getHistory', {'count': 1, 'peer_id': peer_id, 'rev': 0})
    msg_id = history['items'][0]['id']
    #nonlocal msg_id
    return msg_id

def write_msg(peer_id, message):
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'random_id': random.randint(0, 2048), 'disable_mentions': 1})

def edit_msg(peer_id, message, msg_id, **kwargs):
    vk.method('messages.edit', {'peer_id': peer_id, 'message': message, 'message_id': msg_id, "keep_forward_messages": 1})

async def idm_my(delay, peer_id, command, msg_id):
   await asyncio.sleep(delay)
   if ".л мод" in command:
       write_msg(-174105461, "+api (Ваша секретка) https://irisduty.ru/callback")
       edit_msg(peer_id, "Включаю Ваш IDM", msg_id)

async def rehi(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л реши" in command:
    	sms1 = command[5:]
    	sms = f"Ответ: {eval(sms1)}"
    	write_msg(peer_id, sms)

async def wiki(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л вики" in command:
    	text = command[5:]
    	wikipedia.set_lang('ru') 
    	fedr = wikipedia.summary(text)  
    	edit_msg(peer_id, fedr, msg_id)  
    	
async def ping(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л пинг" in command:
	    b = datetime.now().timestamp()
	    a = datetime.now().timestamp()
	    d = str(round(a-b,6))[:-4]
	    sms = f"Пинг данного ЛонгПолла\nПинг: {d}ms"
	    edit_msg(peer_id, sms)
    
async def time(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л время" in command:
    	a = datetime.now(timezone(timedelta(hours=+4))).strftime("Сегодня %d %B %Y (%A)\n Время у Вас - %H:%M \n Хорошего Вам денька!")
    	write_msg(peer_id, a)
    		   
 
def b2s(value: Union[bool, int]) -> str:
    if value:
        return "✅"
    return "🚫"
 
 
    if command.lower().startswith("рр"):
        msg = command[2:]
        history = vk.method(
            'messages.getHistory',
            {
                'count': 1,
                'peer_id': peer_id,
                'rev': 0
            }
        )
 
        id = history['items'][0]['reply_message']['id']
        edit_msg(peer_id, msg, id)
        vk.method("messages.delete", {'message_ids': msg_id, 'delete_for_all': 1})

        	
def bomb(peer_id, message, time):
    vk.method('messages.send',
              {'peer_id': peer_id, 'message': message, 'random_id': random.randint(0, 2048), 'disable_mentions': 1,
               'expire_ttl': time})

        	
async def bomba(delay: float, peer_id: int, command: str, msg_id: int):
    await asyncio.sleep(delay)
 
    if command.lower().startswith(".л б"):
    	time, text = map(str,command[2:].split("|"))
    	arg = time[-1]
    	time = int(time[:-1])
    	if arg == 'ч':
    	    time *= 3600
    	if arg == 'м':
    	   time *= 60
    	if time > 86400:
        	write_msg(peer_id, "Выберете время меньше 24 часов")

    	vk.method("messages.delete", {'message_ids': msg_id, 'delete_for_all': 1})

    	bomb(peer_id, text, time)

async def vls(delay: float, peer_id: int, command: str, msg_id: int):
    await asyncio.sleep(delay)
 
    if command.lower().startswith(".л влс"):
            text = command[4:]
            history = vk.method(
            'messages.getHistory',
            {
                'count': 1,
                'peer_id': peer_id,
                'rev': 0
            })
            user_id = history['items'][0]['reply_message']['from_id']
            user = vk.method(
            'users.get',
            {
                'user_ids': user_id,
                'fields': 'photo_50'
            })[0]
            a = user["id"]
            write_msg(a, text)
            vk.method("messages.delete", {'message_ids': msg_id, 'delete_for_all': 1})

async def scrin(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л скрин" in command:
    	vk.method('messages.sendService', {'peer_id': peer_id, 'action_type': "chat_screenshot", 'random_id': 0})
    	vk.method("messages.delete", {'message_ids': msg_id, 'delete_for_all': 1})


async def admin(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л +админ" in command:
            history = vk.method(
            'messages.getHistory',
            {
                'count': 1,
                'peer_id': peer_id,
                'rev': 0
            })
            id = history['items'][0]['reply_message']['from_id']
            vk.method('messages.setMemberRole', {'peer_id': peer_id, 'member_id': id, 'role': 'admin'})
            edit_msg(peer_id, "Права админа выданы, ъуъ!" , msg_id)

async def admin_delete(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л -админ" in command:
            history = vk.method(
            'messages.getHistory',
            {
                'count': 1,
                'peer_id': peer_id,
                'rev': 0
            })
            id = history['items'][0]['reply_message']['from_id']
            vk.method('messages.setMemberRole', {'peer_id': peer_id, 'member_id': id, 'role': 'member'})
            edit_msg(peer_id, "Вы сняли права админа\n Press, F...", msg_id)



 
 

    if command.lower().startswith("рр"):

        msg = command[2:]

        history = vk.method(

            'messages.getHistory',

            {

                'count': 1,

                'peer_id': peer_id,

                'rev': 0

            }

        )

 

        id = history['items'][0]['reply_message']['id']

        edit_msg(peer_id, msg, id)

        vk.method("messages.delete", {'message_ids': msg_id, 'delete_for_all': 1})

        	def bomb(peer_id, message, time):

    vk.method('messages.send',

              {'peer_id': peer_id, 'message': message, 'random_id': random.randint(0, 2048), 'disable_mentions': 1,

               'expire_ttl': time})

        	

async def bomba(delay: float, peer_id: int, command: str, msg_id: int):

    await asyncio.sleep(delay)
                    # asyncio.run(add_user(0, event.peer_id, command, msg_id))
                    print(command)
                except Exception as error:
                    print(error)
                continue#


