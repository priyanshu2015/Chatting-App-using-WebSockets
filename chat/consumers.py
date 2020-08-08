import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer

from channels.db import database_sync_to_async

from .models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        # to accept the websocket connection request made by the user
        # await because asynchronously so waits till the process ends
        
        other_user = self.scope['url_route']['kwargs']['username']  # from websocket url
        me = self.scope['user']
        # await asyncio.sleep(10)
        # await self.send({
        #     "type": "websocket.send",
        #     "text": "hello"
        # })


        # to get the chat from database
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        print(me, thread_obj.id)

        # making a chatroom
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        
        await self.send({
            "type": "websocket.accept"
        })
    
    # this function will recieve the message sent from client side(websocket)
    async def websocket_receive(self, event):
        print("recieve", event)
        # {'type': 'websocket.receive', 'text': '{"message":"kaise ho?"}'}
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            print(msg)
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
                
            myResponse = {
                'message': msg,
                'username': username            
            }
            # saving message to database
            await self.create_chat_message(user, msg)
            
            
            #for sending messages to all memebers in a chat room
            # broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",   # custom async method defined below
                    "text": json.dumps(myResponse)
                }
            )

            # for sending messages to himself when chat room is not created
            # await self.send({
            #     "type": "websocket.send",
            #     "text": json.dumps(myResponse)
            # })

    # custom method created by ourselves to send message to all members in a group
    async def chat_message(self, event):
        # send the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconneted", event)
    
    @database_sync_to_async    # decorator to get the data from database and syncing with asynchronous calls
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]           # function defined in models.py to get the latest chat between two users
    
    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread = thread_obj, user = me, message = msg)
