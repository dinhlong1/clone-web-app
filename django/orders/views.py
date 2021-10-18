import json
from typing import Dict
from django.db.models import Q, F
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, permissions
from users.models import User
from accounts.models import Account, Category
from .serializers import OrderSerializer, OrdersSerializerAdmin, OrderDetailSerializer, MyOrderSerializer, MyOrderDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from users.models import TransactionUser, User
from users.serializers import TransactionUserSerializer, TransactionUserTopSerializer
from .models import Orders, OrderDetail
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.core import serializers
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
import datetime
from django.db.models import Sum, Count
import requests
from django.db.models.functions import TruncMonth
from django.utils import timezone


def check_live(uid):
    url = "https://graph.facebook.com/{}/picture?type=normal".format(uid)
    response = requests.get(url)
    if "//static" in response.url:
        return False
    else:
        return True


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def payment(request):
    serializer = OrderSerializer(data=request.POST)
    if serializer.is_valid():
        category = Category.objects.get(id=request.POST.get("category", ""))
        quantity = int(request.POST.get("quantity", ""))
        user = User.objects.get(id=request.POST.get("user", ""))

        paid_amount = int((int(category.price) * quantity)
                          * (100 - category.discount)/100)

        if quantity > category.get_quantity():
            t = TransactionUser.objects.create(users=user, description="Thanh toán mua hàng thất bại", option=4,
                                               money=paid_amount, confirm=False)
            t.save()
            return Response("Số lượng sản phẩm mua không hợp lệ", status=status.HTTP_400_BAD_REQUEST)
        if user.coin < paid_amount:
            t = TransactionUser.objects.create(users=user, description="Thanh toán mua hàng thất bại", option=4,
                                               money=paid_amount, confirm=False)
            t.save()
            return Response("Số Coin Không Đủ Để Thanh Toán", status=status.HTTP_400_BAD_REQUEST)
        try:
            user.coin -= paid_amount
            user.save()
            items = []
            target = quantity
            while target != 0:
                listAccounts = Account.objects.filter(
                    category__id=category.id, sold=False)[:target]
                for item in listAccounts:
                    if check_live(item.uid):
                        items.append(item)
                        item.sold = True
                    else:
                        item.status = False
                    item.save()
                target = quantity - len(items)

            serializer.save(paid_amount=paid_amount, items=items)
            t = TransactionUser.objects.create(
                users=user, description="Thanh toán mua hàng thành công", option=4, money=paid_amount, confirm=True)
            t.save()
            return Response("Thanh toán thành công", status=status.HTTP_201_CREATED)
        except Exception:
            t = TransactionUser.objects.create(users=user, description="Thanh toán mua hàng thất bại", option=4,
                                               money=paid_amount, confirm=False)
            t.save()
            return Response("Lỗi thanh toán không thành công", status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        queryset = Orders.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = MyOrderSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TransactionsList(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        queryset = TransactionUser.objects.filter(users=request.user)
        page = self.paginate_queryset(queryset)
        serializer = TransactionUserSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def ShowDetail(request):
    if Orders.objects.get(id=request.POST.get("order", ""), user=request.user):
        try:
            resuilt = ''
            items = OrderDetail.objects.filter(
                order_id=request.POST.get("order", ""))
            for item in items:
                account = []
                account.append(item.account.uid)
                account.append(item.account.password)
                if item.account.auth != None:
                    account.append(item.account.auth)
                if item.account.email != None:
                    account.append(item.account.email)
                if item.account.password_email != None:
                    account.append(item.account.password_email)
                if item.account.token != None:
                    account.append(item.account.token)
                if item.account.cookie != None:
                    account.append(item.account.cookie)

                resuilt += "|".join(account) + "\n"
            response = HttpResponse(resuilt, content_type='application/json;')
            response['Content-Disposition'] = 'attachment; filename="data.txt"'
            return response
        except Exception:
            return Response("Dữ liệu không tồn tại", status=status.HTTP_400_BAD_REQUEST)
    return Response("Lỗi xác thực", status=status.HTTP_400_BAD_REQUEST)


class OrdersListAdmin(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    # @authentication_classes([JWTAuthentication])
    def list(self, request):
        queryset = Orders.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = OrdersSerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)


@permission_classes([permissions.IsAdminUser])
@authentication_classes([JWTAuthentication])
class OrdersDetailListAdmin(viewsets.GenericViewSet):
    def list(self, request):
        queryset = OrderDetail.objects.filter(order__id=request.GET['id'])
        page = self.paginate_queryset(queryset)
        serializer = OrderDetailSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SearchOrder(viewsets.GenericViewSet):
    def list(self, request):
        query = request.GET["query"]
        if query:

            queryset = Orders.objects.filter(Q(user__email__icontains=query)|Q(category__name__icontains=query)|Q(quantity__icontains=query)|Q(paid_amount__icontains=query)|Q(created_at__icontains=query))

        else:
            queryset = Orders.objects.all()

        #
        page = self.paginate_queryset(queryset)

        serializer = OrdersSerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([JWTAuthentication])
def DashBoardViews(request):
    today = timezone.now()
    year = today.year
    month = today.month
    if request.method == "POST":
        # Get Sales  in month
        salesOld = Orders.objects.exclude(created_at__lt=datetime.date(
            year, month - 1, 1)).aggregate(salesOld=Sum('quantity'))
        sales = Orders.objects.exclude(created_at__lt=datetime.date(
            year, month, 1)).aggregate(sales=Sum('quantity'))

        # Get Profit  in month
        profitOld = Orders.objects.exclude(created_at__lt=datetime.date(
            year, month - 1, 1)).aggregate(profitOld=Sum('paid_amount'))
        profit = Orders.objects.exclude(created_at__lt=datetime.date(
            year, month, 1)).aggregate(profit=Sum('paid_amount'))

        # Get Total User  in month
        totalUserOld = User.objects.exclude(date_joined__gt=datetime.date(
            year, month, 1)).aggregate(totalUserOld=Count('email'))
        totalUser = User.objects.aggregate(totalUser=Count('email'))

        # Get Total Coin recharger  in month
        coinRechargeOld = TransactionUser.objects.exclude(created_at__lt=datetime.date(
            year, month - 1, 1), option="1").aggregate(coinRechargeOld=Sum('money'))
        coinRecharge = TransactionUser.objects.exclude(created_at__lt=datetime.date(
            year, month, 1), option="1").aggregate(coinRecharge=Sum('money'))

        # Get Info User get email and money
        list = TransactionUser.objects.exclude(created_at__lt=datetime.date(
            year, month, 1)).exclude(option="4").exclude(option="3").exclude(option="2")
        Transactionserializer = TransactionUserTopSerializer(list, many=True)

        target = []

        # Convert OrderedDict to dict
        for item in Transactionserializer.data:
            target.append([{'users': dict(item['users'])},
                          {'money': item['money']}])

        topUserRecharge = []

        # Distinct by User
        for i in target:
            if topUserRecharge == []:
                topUserRecharge.append(i)
            else:
                flag = 0
                for t in topUserRecharge:
                    if t[0]['users']['id'] == i[0]['users']['id']:
                        t[1]['money'] += i[1]['money']
                        flag = 1
                        break
                if flag == 0:
                    topUserRecharge.append(i)
        topUserRecharge.sort(key=lambda x: x[1]['money'], reverse=True)


        # Add all to dict
        resuilt = [{"topUserRecharge": topUserRecharge[:5]}, salesOld, sales,
                   profitOld, profit, totalUserOld, totalUser, coinRechargeOld, coinRecharge]

        # Get recent purchase
        recentPurchaseList = Orders.objects.all()[:5]
        serializer = OrdersSerializerAdmin(recentPurchaseList, many=True)

        # append data to dict
        resuilt.append(serializer.data)
        
        # Top 5  purchase
        purchaseList = Orders.objects.exclude(created_at__lt=datetime.date(year, month, 1)).order_by('-paid_amount')[:5]
        serializer = OrdersSerializerAdmin(purchaseList, many=True)
        # append data to dict
        resuilt.append(serializer.data)

        return Response(resuilt, status=status.HTTP_201_CREATED)

    return Response("thất bại", status=status.HTTP_400_BAD_REQUEST)
