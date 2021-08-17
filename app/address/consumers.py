from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
import time
import asyncio
import traceback
from .vendor.venderFactory import VendorFactory
from .errors.consumer_exceptions import ConsumerException
import logging
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
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

        # 사이트 오픈
        try:
            status, message = vendor_obj.open_site()
            await self.send(text_data=json.dumps({
                'message': message,
                'status': status,
                'index': index
            }))
            await asyncio.sleep(1)
            # 로그인
            status, message = vendor_obj.execute_login_page()
            await self.send(text_data=json.dumps({
                'message': message,
                'status': status,
                'index': index
            }))
            await asyncio.sleep(1)
            # 주소 변경
            status, message = vendor_obj.execute_address_page()
            await self.send(text_data=json.dumps({
                'message': message,
                'status': status,
                'index': index
            }))
            await asyncio.sleep(1)
            await self.send(text_data=json.dumps({
                'message': '완료',
                'status': status,
                'index': index
            }))
        except AssertionError as e:
            if isinstance(e, ConsumerException):
                await self.send(text_data=json.dumps({
                    'message': e.msg,
                    'status': e.status,
                    'index': index
                }))
        except Exception:
            logger.error(traceback.format_exc())
            await self.send(text_data=json.dumps({
                'message': 'error 발생',
                'status': False,
                'index': index
            }))

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
