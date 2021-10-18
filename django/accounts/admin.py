from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Category, Account
# Register your models here.

admin.site.unregister(Group)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount", "get_quantity","created_at","updated_at")
    fields = ["name", ("price",  "discount"), "quantity"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('uid', 'password', 'auth', 'email', 'password_email',"category", "sold", "status","created_at")
    fields = ["category",('uid', 'password'), 'auth', ('email', 'password_email'),"token","cookie","sold","status"]