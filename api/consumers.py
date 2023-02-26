from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import  json
# from channels.generic.websocket import AsyncWebsocketConsumer
#
# class MyConsumer(AsyncWebsocketConsumer):
#     groups = ["broadcast"]
#
#     async def connect(self):
#         # Called on connection.
#         # To accept the connection call:
#         await self.accept()
#         # Or accept the connection and specify a chosen subprotocol.
#         # A list of subprotocols specified by the connecting client
#         # will be available in self.scope['subprotocols']
#         await self.accept("subprotocol")
#         # To reject the connection, call:
#         await self.close()
#
#     async def receive(self, text_data=None, bytes_data=None):
#         # Called with either text_data or bytes_data for each frame
#         # You can call:
#         await self.send(text_data="Hello world!")
#         # Or, to send a binary frame:
#         await self.send(bytes_data="Hello world!")
#         # Want to force-close the connection? Call:
#         await self.close()
#         # Or add a custom WebSocket error code!
#         await self.close(code=4123)
#
#     async def disconnect(self, close_code):
#         pass
        # Called when the socket closes
# class MyConsumer(WebsocketConsumer):
#     groups = ["broadcast"]
#
#     def connect(self):
#         # Called on connection.
#         # To accept the connection call:
#         self.accept()
#         # Or accept the connection and specify a chosen subprotocol.
#         # A list of subprotocols specified by the connecting client
#         # will be available in self.scope['subprotocols']
#         self.accept("subprotocol")
#         # To reject the connection, call:
#         self.close()
#
#     def receive(self, text_data=None, bytes_data=None):
#         # Called with either text_data or bytes_data for each frame
#         # You can call:
#         self.send(text_data="Hello world!")dump
#         # Or, to send a binary frame:
#         self.send(bytes_data="Hello world!")
#         # Want to force-close the connection? Call:
#         self.close()
#         # Or add a custom WebSocket error code!
#         self.close(code=4123)
#
#     def disconnect(self, close_code):
#         pass
#         # Called when the socket closes
class StripeCheckoutConsumer(WebsocketConsumer):
    def connect(self):
        #TODO
        # self.room_name=self.scope['url_route']['kwargs']['user_id']
        # self.room_group_name='checkout_%s' % self.room_name
        self.room_name='test_room'
        self.room_group_name='test_group'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        self.accept()
        self.send(text_data=json.dumps(
            {'status':'connected'}
        ))

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def send_task_completed_signal(self,event):
        print(event.get('value'))
        self.send(text_data=json.dumps(event.get('value')
        ))