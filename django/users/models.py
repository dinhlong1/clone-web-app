from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    coin = models.IntegerField(default=0)
    ip = models.CharField(max_length=16, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["coin"]

    objects = UserManager()

    def __str__(self):
        return self.email


class TransactionUser(models.Model):
    TRANSACTION_TYPE_OPTION = (
        ('1', 'Recharge '),
        ('2', 'Increase '),
        ('3', 'Discount'),
        ('4', 'Decrease')
    )

    users = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=400, null=True, blank=True)
    # ip = models.CharField(max_length=16, blank=True, null=True)
    option = models.CharField(max_length=1, choices=TRANSACTION_TYPE_OPTION)
    money = models.IntegerField(null=False, blank=False)
    confirm = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', ]

    def transaction_option(self):
        user = User.objects.get(id=self.users)
        if self.option == "1":
            user.coin += self.money
        elif self.option == "2":
            user.coin += self.money
        elif self.option == "2":
            user.coin += self.money
        else:
            user.coin -= self.money

    def __str__(self):
        return '%s' % self.id
