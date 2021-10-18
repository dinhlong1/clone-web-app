from rest_framework import serializers

from .models import User, TransactionUser
from django.contrib.auth.models import update_last_login

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_superuser'] = user.is_superuser
        update_last_login(None, user) 
        
        return token
class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('id',  'email', 'coin')


class UserSerializerAdmin(serializers.ModelSerializer):
    # profile = ProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('id',  'email', 'password', 'coin',
                  'date_joined', 'last_login')

class TransactionUserTopSerializer(serializers.ModelSerializer):
    users = UserSerializer()
    class Meta:
        model = TransactionUser
        fields = (
            'users',
            'money'
         )

class TransactionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionUser
        fields = (
            'description',
            'option',
            'money',
            'confirm',
            'created_at'
        )

class TransactionUserSerializerAdmin(serializers.ModelSerializer):
    users = UserSerializer()
    class Meta:
        model = TransactionUser
        fields = (
            'users',
            'description',
            'option',
            'money',
            'confirm',
            'created_at'
        )