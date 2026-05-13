from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Prefetch
from .models import Item, ShoppingList

def index(request):
    # Traemos todas las listas con sus ítems que NO han sido comprados
    lists = ShoppingList.objects.prefetch_related(
        Prefetch('items', queryset=Item.objects.filter(is_done=False).order_by('-created_at'))
    ).order_by('-created_at')
    
    return render(request, 'core/index.html', {'lists': lists})

def add_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        new_list = ShoppingList.objects.create(name=name)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'shopping_list',
            {
                'type': 'list_update', # Nuevo evento para listas
                'action': 'add_list',
                'list': {
                    'id': new_list.id,
                    'name': new_list.name,
                }
            }
        )
        return JsonResponse({'status': 'ok'})

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        list_id = request.POST.get('list_id')
        # Lo convertimos a entero de forma segura
        quantity = int(request.POST.get('quantity', 1)) 
        image = request.FILES.get('image')

        shopping_list = ShoppingList.objects.get(id=list_id)
        item = Item.objects.create(name=name, shopping_list=shopping_list, image=image, quantity=quantity)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'shopping_list',
            {
                'type': 'item_update',
                'action': 'add',
                'item': {
                    'id': item.id,
                    'name': item.name,
                    'quantity': item.quantity,
                    'list_id': shopping_list.id,
                    'image_url': item.image.url if item.image else ''
                }
            }
        )
        return JsonResponse({'status': 'ok'})