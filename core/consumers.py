import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Item

class ShoppingListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'shopping_list'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Recibe mensajes del Frontend
    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'mark_done':
            item_id = data['item_id']
            await self.mark_item_done(item_id)
            
            # Avisar a todos que el ítem fue comprado
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'item_update',
                    'action': 'done',
                    'item_id': item_id
                }
            )

    @database_sync_to_async
    def mark_item_done(self, item_id):
        Item.objects.filter(id=item_id).update(is_done=True)

    # Envía mensajes al Frontend
    async def item_update(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def list_update(self, event):
        await self.send(text_data=json.dumps(event))
        