from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField()
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:detail", kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'pk': self.pk})
    

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return "%s of %s" %(self.quantity, self.item.name)

    def get_total_item_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_address = models.ForeignKey("Address", on_delete=models.SET_NULL, blank=True, null=True)
    received = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username