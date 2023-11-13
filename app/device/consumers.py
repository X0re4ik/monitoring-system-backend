from channels.generic.websocket import WebsocketConsumer


class JoinAndLeave(WebsocketConsumer):
    def connect(self):
        print(self.scope)
        print("server says connected")

    def receive(self, text_data=None, bytes_data=None):
        print("server says client message received: ", text_data)
        self.send("Server sends Welcome")

    def disconnect(self, code):
        print("server says disconnected")


from channels.consumer import AsyncConsumer


import json
from channels.db import database_sync_to_async
from device.models import Device, Measurement

from device.serializers import MeasurementSerializer


from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer


class RetrievingMeasurementData(WebsocketConsumer):
    
    
    def connect(self):
        self._mac_address = str(self.scope['url_route']['kwargs']["mac_address"])
        self.room_group_name = str(f"measurement_{self._mac_address}")
        self._device = Device.objects.get(pk=self._mac_address)
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    
    def receive(self, text_data):
        measurement = Measurement.objects.filter(device=self._device).last()
        data = json.dumps(MeasurementSerializer(measurement).data)
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_data',
                'message': data,
            }
        )
    
    def send_data(self, event):
        self.send(text_data=json.dumps({
            'event': "Send",
            'message': event["message"]
        }))
        
