from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
import time
import asyncio
from .vendor.venderFactory import VendorFactory


class ChatConsumer(AsyncWebsocketConsumer):
    # def connect(self):
    #     self.accept()

    # def disconnect(self, close_code):
    #     pass

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))
    # def connect(self):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        # await async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        # await sync_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        '''
            {'object': {'vendor': 'musinsa', 'vendor_id': 'saecomaster', 'vendor_password': 'sksmssk12!', 'postcode': '06540', 'address': '서울특별시 서초구 주흥길 14', 'details': '305호', 'recipient': '나경원', 'shipping_address': '우리집', 'phone_number_head': '010', 'phone_number_middle': '9044', 'phone_number_tail': '8972'}}
        '''
        text_data_json = json.loads(text_data)
        vendor_object = text_data_json['object']
        vendor = vendor_object['vendor']
        index = vendor_object['index']
        factory = VendorFactory()
        vendor_obj = factory.getVendor(vendor, **vendor_object)
        status, message = vendor_obj.open_site()
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message,
        #         'status': status,
        #         'index': index
        #     }
        # )
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status,
            'index': index
        }))
        await asyncio.sleep(1)
        status, message = vendor_obj.execute_login_page()
        if not status:
            return
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status,
            'index': index
        }))
        await asyncio.sleep(1)
        status, message = vendor_obj.execute_address_page()
        if not status:
            return
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status,
            'index': index
        }))
        await asyncio.sleep(1)
        if not status:
            return
        if status:
            await self.send(text_data=json.dumps({
                'message': '변경 성공!',
                'status': status,
                'index': index
            }))
        # login
        # await asyncio.sleep(4)
        # await asyncio.sleep(5)
        # await self.send(text_data=json.dumps({
        #     'message': message,
        #     'status': status,
        #     'index': index
        # }))
        # status, message = vendor_obj.execute_login_page()
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message,
        #         'status': status,
        #         'index': index
        #     }
        # )

        # address
        # finish

        # Send message to room group

    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']
        status = event['status']
        index = event['index']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status,
            'index': index
        }))
