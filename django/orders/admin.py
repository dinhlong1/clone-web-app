from django.contrib import admin
from .models import Orders,OrderDetail
# Register your models here.
admin.site.register(Orders)
# admin.site.register(OrderDetail)

# @admin.register(Orders)
# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ("transation_id",'user', "category", "paid_amount", "get_quantity", "created_at")
#     fields = ['user',"category", "paid_amount", "quantity"]

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', "account", "created_at")
    fields = ['order',"account"]