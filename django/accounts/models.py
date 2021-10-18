from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    discount = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    def get_quantity(self):
        list = Account.objects.filter(category__name=self.name, sold=False)
        self.quantity = len(list)
        self.save()
        return self.quantity

    def total_quantity(self):
        total = len(Account.objects.filter(category__name=self.name))
        return total

    def sale_figure(self):
        total = len(Account.objects.filter(
            category__name=self.name, sold=True))
        return total

    def __str__(self):
        return self.name


class Account(models.Model):
    category = models.ForeignKey(
        Category, related_name="accounts", on_delete=models.CASCADE)
    uid = models.CharField(max_length=32, null=False,
                           blank=False)
    password = models.CharField(max_length=20, null=True, blank=False)
    auth = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password_email = models.CharField(max_length=20, null=True, blank=True)
    cookie = models.CharField(max_length=300, null=True, blank=True)
    token = models.CharField(max_length=50, null=True, blank=True)
    sold = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ['sold']
        unique_together = (("uid", "id"),)

    def __str__(self):
        return self.uid
