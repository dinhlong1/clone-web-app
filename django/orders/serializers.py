from rest_framework import serializers
from accounts.serializers import AccountSerializer
from users.serializers import UserSerializer
from .models import Orders, OrderDetail
from users.models import TransactionUser
from accounts.models import Account
from accounts.serializers import CategorySerializer


class MyOrderDetailSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)

    class Meta:
        model = OrderDetail
        fields = (
            'accounts',
        )


class MyOrderSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Orders
        fields = (
            "id",
            "category",
            # "categories",
            "quantity",
            "paid_amount",
            "created_at"
        )


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = (
            "id",
            "user",
            "category",
            "quantity",
        )

    def create(self, validated_data):

        items_data = validated_data.pop('items')
        order = Orders.objects.create(**validated_data)
        for item_data in items_data:
            OrderDetail.objects.create(order=order, account=item_data)

        return order


class OrdersSerializerAdmin(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()

    class Meta:
        model = Orders
        fields = (
            "id",
            "user",
            "category",
            "quantity",
            "paid_amount",
            "created_at"
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    account = AccountSerializer()

    class Meta:
        model = OrderDetail
        fields = (
            'order',
            'account',
        )
