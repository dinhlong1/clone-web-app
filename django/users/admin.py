from django.contrib import admin
from .models import User, TransactionUser
# Register your models here.

admin.site.register(User)
admin.site.register(TransactionUser)