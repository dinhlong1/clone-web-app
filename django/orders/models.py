from django.db import models
from users.models import User
from accounts.models import Category, Account
# Create your models here.


class Orders(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    paid_amount = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_quantity(self):
        self.quantity = len(OrderDetail.objects.get(order__id=self.id))

        return self.quantity

    def __str__(self):
        return '%s' % self.id


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.id
