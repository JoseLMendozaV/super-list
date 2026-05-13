from django.db import models

class ShoppingList(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # Ahora es un IntegerField numérico
    quantity = models.IntegerField(default=1) 
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.name} - {self.shopping_list.name}"