from django.contrib import admin
from .models import Pet, Cart, CartItems, CustomUser

# Register your models here.
admin.site.register(Pet)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(CustomUser)