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
import locale
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
    	write_msg(peer_id, fedr, msg_id)  
    	
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
 
 
async def user(delay: float, peer_id: int, command: str, msg_id: int):
    await asyncio.sleep(delay)
 
    if command.lower().startswith(".л кто"):
        history = vk.method(
            'messages.getHistory',
            {
                'count': 1,
                'peer_id': peer_id,
                'rev': 0
            }
        )
 
        user_id = history['items'][0]['reply_message']['from_id']
        url = f'https://vk.com/foaf.php?id={user_id}'
        response = (urllib.request.urlopen(url)).read()
        soup = BeautifulSoup(response, "html.parser")
        date = re.search('<ya:created dc:date="(.+)"></ya:created>', str(soup))
        date = (date.group().split('"')[1])
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        new_date = datetime.strftime(dt, '%d.%m.%Y')
        date_reg = str(new_date)

        user = vk.method(
            'users.get',
            {
                'user_ids': user_id,
                'fields': 'photo_50,status,bdate,blacklisted_by_me,'
                          'blacklisted,photo_max_orig,is_friend,'
                          'last_name_abl,first_name_abl,domain,'
                          'city,followers_count,last_seen,online,sex,is_closed'
            }
        )[0]
        city_name: str = user.get('city', {}).get('title', "Мухосранск")
        followers: str = user.get('followers_count', "Их нет...")
        date_dr: str = user.get('bdate', "Ты когда родился?0_о")
        platform = user.get('last_seen', {}).get('platform', "Не официальное ПО")
 
        user["blacklisted_by_me"] = b2s(user["blacklisted_by_me"])
        user["blacklisted"] = b2s(user["blacklisted"])
        user["is_closed"] = b2s(user["is_closed"])
        user["is_friend"] = b2s(user["is_friend"])
        user["online"] = 'Online' if user["online"] else 'Offline'
 
        if user['sex'] == 1:
            user['sex'] = "👱‍♀️"
        elif user['sex'] == 2:
            user['sex'] = "👨"
        else:
            user["sex"] = "Ламинат"

 
        msg = f"""
        Информация о {user["first_name_abl"]} {user["last_name_abl"]}
        {user["online"]}, {platform}
 
        ID: {user["id"]}
        Короткая ссылка: {user["domain"]}
        Имя: {user["first_name"]}
        Фамилия: {user["last_name"]}
        Дата регистрации: {date_reg}
        Дата рождение: {date_dr}
        Город: {city_name}
        Друзья: {user["is_friend"]}
        Подписчики: {followers}
        Пол: {user["sex"]}
        Закрытый прoфиль: {user["is_closed"]}
        Статус: {user["status"]}
        Я в чс: {user["blacklisted"]}
        Он в чс: {user["blacklisted_by_me"]}
        Фото:
        {user["photo_max_orig"]}
        """.replace('    ', '')
        edit_msg(peer_id, msg, msg_id)
        
async def rr(delay: float, peer_id: int, command: str, msg_id: int):
    await asyncio.sleep(delay)
 
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
 
    if command.lower().startswith(".влс"):
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




async def trans(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л гс" in command:
        audio = vk.method(
            'messages.getHistory',
            {
                'count': 1,
                'peer_id': peer_id,
                'rev': 0
            }
        )
        
        user_id = audio['items'][0]['reply_message']['from_id']
        
        user = vk.method(
            'users.get',
            {
                'user_ids': user_id,
                'fields': 'photo_50'
            })[0]
        
        text = audio['items'][0]['reply_message']['attachments'][0]['audio_message']['transcript']
        msg = f"""
        ✉️Голосовое сообщение от {user["first_name"]} {user["last_name"]}
💬Перевод от ВКонтакте:
        {text}
        """.replace('    ', '')
        edit_msg(peer_id, msg, msg_id)

def attachments(peer_id):
    history = vk.method('messages.getHistory', {'count': 1, 'peer_id': peer_id, 'rev': 0})

    attachments = []
    for attachment in history['items'][0]['attachments']:
        a_type = attachment['type']
        if a_type in ['link']:
            continue
        attachments.append(
            f"{a_type}{attachment[a_type]['owner_id']}_{attachment[a_type]['id']}_{attachment[a_type]['access_key']}"
        )

    return attachments

def edita_msg(peer_id, message, attachments, msg_id, **kwargs):
    data = {'peer_id': peer_id, 'message': message, 'attachment': attachments, 'message_id': msg_id}
    data.update(kwargs)
    vk.method('messages.edit', data)


async def dd_sms(delay, peer_id, command, msg_id):
    await asyncio.sleep(delay)
    if ".л ддвсе" in command or ".л дд" in command:
        history: Optional[Any] = vk.method('messages.getHistory',
                                           {'count': 1, 'peer_id': peer_id, 'rev': 0})
        msg_text: object = history['items'][0]['text']
        peer_id: object = peer_id
        user_id: Optional[Any] = vk.method('users.get', {})
        user_id = user_id[0]['id']
        regexp: str = r"(^[\S]+)|([\S]+)|(\n[\s\S \n]+)"
        _args: List[Any] = re.findall(str(regexp), str(msg_text))
        args = []
        for arg in _args:
            if arg[1] != '':
                args.append(arg[1])
        if len(args) == 1:
            msg_ids: List[str] = []
            for mmsg in vk_info.get_all_history_gens(peer_id):
                if datetime.now().timestamp() - mmsg['date'] > 86400:
                    break
                if mmsg['from_id'] == user_id and None == mmsg.get('action', None):
                    msg_ids.append(str(mmsg['id']))
            try:
                vk.method("messages.delete", dict(message_ids=",".join(msg_ids), delete_for_all=1))
            except:
                message_id = write_msg(peer_id, f"❗ Не удалось удалить сообщения.")

            t = Timer(2, delete_msg(msg_ids), message_id)
            t.start()
        else:
            argss = args[1:]
            count = ''.join(argss)
            count = int(count)
            msg_ids = []
            for mmsg in vk_info.get_all_history_gen_dd(peer_id):
                if datetime.now().timestamp() - mmsg['date'] > 86400:
                    break
                if mmsg['from_id'] == user_id and None == mmsg.get('action', None):
                    msg_ids.append(str(mmsg['id']))

            msg_idss = []
            for i in range(count):
                msg_idss.append(msg_ids[i])
                edit_msg(peer_id, "&#13;", msg_ids[i])
            message_id = 0
            print(msg_idss)
            try:
                vk.method("messages.delete", {'message_ids': ",".join(msg_idss), 'delete_for_all': 1})
            except:
                message_id = write_msg(peer_id, f"❗ Не удалось удалить сообщения.")

            t = Timer(2, delete_msg(msg_idss), message_id)
            t.start()
while True:  
    token =  "Ваш Токен от вк ме"

    # Авторизуемся как сообщество
    vk = vk_api.VkApi(app_id=6146827, token=token)

    # Работа с сообщениями
    longpoll = VkLongPoll(vk, wait=0)

    # Основной цикл
    for event in longpoll.listen():

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:
        
            if event.from_me:
                msg_id = info_msg_id(event.peer_id)
                command = event.text
                try:
                    # Сообщение от пользователя
                    # kirill.py
                    asyncio.run(idm_my(0, event.peer_id, command, msg_id)) #1.  Переключатель дежурного №1
                    asyncio.run(rehi(0, event.peer_id, command, msg_id))#2.  Калькулятор
                    asyncio.run(ping(0, event.peer_id, command, msg_id))#3.  Пинг
                    asyncio.run(time(0, event.peer_id, command, msg_id))#4.  Время
                    asyncio.run(scrin(0, event.peer_id, command, msg_id))#5.  Липовый скрин                    
                    asyncio.run(wiki(0, event.peer_id, command, msg_id))#6.  Википедея
		    asyncio.run(user(0, event.peer_id, command, msg_id))

                    # admin_chat
                    asyncio.run(admin(0, event.peer_id, command, msg_id))#11.  Выдать права админа
                    asyncio.run(admin_delete(0, event.peer_id, command, msg_id))#12.  Снять права админа                     

                    # asyncio.run(add_user(0, event.peer_id, command, msg_id))
                    print(command)
                except Exception as error:
                    print(error)
                continue#



