from channels.generic.websocket import AsyncWebsocketConsumer
import json
import os
import django
from channels.db import database_sync_to_async
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from .models import chat_sms
from django.utils import timezone
from datetime import datetime

class MyConsumer(AsyncWebsocketConsumer):
    active_connections = set()
    name = {}
    name_list = set()
    async def connect(self):
        # Добавляем текущее подключение в набор активных подключений
        MyConsumer.active_connections.add(self.channel_name)
        MyConsumer.name[self.channel_name] = ''

        await self.accept()

    async def disconnect(self, close_code):
        # Удаляем текущее подключение из набора активных подключений
        if MyConsumer.name[self.channel_name] in MyConsumer.name_list:
             MyConsumer.name_list.remove(MyConsumer.name[self.channel_name])
        del MyConsumer.name[self.channel_name]
        MyConsumer.active_connections.remove(self.channel_name)


    async def receive(self, text_data):
        # Обработка полученных данных
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        typer = text_data_json['registr']
        mas = ''
        if typer:
            sms_all =  await self.get_all_messages()
            MyConsumer.name[self.channel_name] = message
            MyConsumer.name_list.add(message)
            for name2 in MyConsumer.name_list:
                mas += '<p>'+str(name2)+'</p>'
            await self.send(text_data = json.dumps({
            'message':'regOK',
            'name_online':mas,
            'sms_all': sms_all 
            }))
        else:
         await self.send_to_all(message,MyConsumer.name[self.channel_name])

    async def send_to_all(self, message,name):

        date = datetime.now()
        await self.save_user_sms(name,message,date)

        for channel_name in MyConsumer.active_connections:
            await self.channel_layer.send(channel_name, {
                'type': 'chat_message',
                'message': message,
                'name': name,
            })
           
    async def chat_message(self, event):
        message = event['message']
        name = event['name']
        mas = ''
        for name2 in MyConsumer.name_list:
            mas += '<p>'+str(name2)+'</p>'
        await self.send(text_data=json.dumps({
            'message': message,
            'name': name,
            'name_online':mas
        }))
    
    async def send_message_to_user(self, channel_name, message):
        await self.channel_layer.send(channel_name, {
            'type': 'chat_message',
            'message': message
        })
    
    
    @database_sync_to_async
    def get_all_messages(self):
            messages = chat_sms.objects.all()
            all_sms = ''
            print( str(all_sms))
            for mess in messages:
                name_bd = mess.name
                time_bd = mess.date.strftime("%H:%M")
                sms = mess.sms_text
                all_sms += f'<div class="sms"><div class="name__user">{name_bd}</div><div class="dekor"><p class="sms__text">{sms}</p></div><div class="time">{time_bd}</div></div>'
            return all_sms
    @database_sync_to_async
    def save_user_sms(self,name,sms,date):
        new_message = chat_sms(name=name, sms_text=sms, date=date)
        new_message.save()
        return