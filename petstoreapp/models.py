from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
"""class MyUser(AbstractUser):
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)"""

class CustomUser(AbstractUser):
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{ self.name }"

class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{ self.name }"
    
class Cart(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.user.username }"
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        f"{ self.quantity } * { self.pet.name } in cart for {self.cart.user.username }"