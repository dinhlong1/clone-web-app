from rest_framework import serializers

from .models import Category, Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'uid',
            'password',
            'auth',
            'email',
            'password_email',
            'cookie',
            'token',
            'status',
            'sold'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            "name",
            "price",
            "discount",
            "get_quantity",
            # "sale_figure ",
        )


class CategorySerializerAdmin(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            "name",
            "price",
            "discount",
            "get_quantity",
            "total_quantity",
            "sale_figure",
            "created_at",
            "updated_at"
        )
