import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Item, ShoppingList

class ShoppingListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'shopping_list'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        # --- ACCIONES PARA ÍTEMS ---
        if action == 'mark_done':
            await self.mark_item_done(data['item_id'])
            await self.broadcast_item_action('done', data['item_id'])

        elif action == 'delete_item':
            await self.delete_item_db(data['item_id'])
            await self.broadcast_item_action('delete', data['item_id'])

        elif action == 'edit_item':
            await self.edit_item_db(data['item_id'], data['new_name'])
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'item_update', 'action': 'edit', 'item_id': data['item_id'], 'new_name': data['new_name']}
            )
            
        elif action == 'update_quantity':
            await self.update_quantity_db(data['item_id'], data['new_quantity'])
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'item_update', 'action': 'update_qty', 'item_id': data['item_id'], 'new_quantity': data['new_quantity']}
            )

        # --- ACCIONES PARA LISTAS ---
        elif action == 'delete_list':
            await self.delete_list_db(data['list_id'])
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'list_update', 'action': 'delete', 'list_id': data['list_id']}
            )

        elif action == 'edit_list':
            await self.edit_list_db(data['list_id'], data['new_name'])
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'list_update', 'action': 'edit', 'list_id': data['list_id'], 'new_name': data['new_name']}
            )

    # --- FUNCIONES DE BASE DE DATOS (SÍNCRONAS) ---
    @database_sync_to_async
    def mark_item_done(self, item_id):
        Item.objects.filter(id=item_id).update(is_done=True)

    @database_sync_to_async
    def delete_item_db(self, item_id):
        Item.objects.filter(id=item_id).delete()

    @database_sync_to_async
    def edit_item_db(self, item_id, new_name):
        Item.objects.filter(id=item_id).update(name=new_name)
        
    @database_sync_to_async
    def update_quantity_db(self, item_id, new_quantity):
        Item.objects.filter(id=item_id).update(quantity=new_quantity)

    @database_sync_to_async
    def delete_list_db(self, list_id):
        ShoppingList.objects.filter(id=list_id).delete()

    @database_sync_to_async
    def edit_list_db(self, list_id, new_name):
        ShoppingList.objects.filter(id=list_id).update(name=new_name)

    # --- EMISORES (BROADCAST) ---
    async def broadcast_item_action(self, action, item_id):
        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'item_update', 'action': action, 'item_id': item_id}
        )

    async def item_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def list_update(self, event):
        await self.send(text_data=json.dumps(event))