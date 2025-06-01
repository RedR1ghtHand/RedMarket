from django.db import models
from django.utils import timezone
from app_item.models import ItemType, Material, Enchantment
from app_account.models import User


class Order(models.Model):
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    enchantments = models.ManyToManyField(Enchantment, through='OrderEnchantment')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.created_by.mc_username} Selling: {self.material.name} {self.item_type.name} for {self.price} (x{self.quantity})"

    def soft_delete(self):
        """Mark order as deleted instead of removing it from database"""
        self.deleted_at = timezone.now()
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None


class OrderEnchantment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    enchantment = models.ForeignKey(Enchantment, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1)
