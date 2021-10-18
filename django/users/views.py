from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import User, TransactionUser
from .serializers import UserSerializer, UserSerializerAdmin, TransactionUserSerializerAdmin, MyTokenObtainPairSerializer
# Create your views here.
from rest_framework import viewsets
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView


class MyProfile(generics.RetrieveAPIView):
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([JWTAuthentication])
    def get(self, request):
        users_id = Token.objects.get(key=request).user_id
        profile = User.objects.get(id=users_id)
        serializer = UserSerializer(profile, many=True)
        return Response(data=serializer.data)


class UserList(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        queryset = User.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = UserSerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)


class UserDetail(APIView):
    @ permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def get(self, request, id, format=None):
        try:
            user = User.objects.filter(id=id)
            serializer = UserSerializerAdmin(user, many=True)
            return Response(data=serializer.data)
        except Exception:
            return Response("Tài khoản không tồn tại", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
@ permission_classes([permissions.IsAdminUser])
@authentication_classes([JWTAuthentication])
def UserViews(request):
    if request.method == "PUT":
        try:
            email = request.POST["email"]
            coin = int(request.POST["coin"])
            user = User.objects.get(id=int(request.POST.get("id", "")))
            user.email = email
            if coin > user.coin:
                t = TransactionUser.objects.create(
                    users=user, description="Cộng tiền vào tài khoản", option=1, money=coin - user.coin, confirm=True)
                t.save()
            if coin < user.coin:
                t = TransactionUser.objects.create(
                    users=user, description="Trừ tiền từ tài khoản", option=2, money=user.coin - coin, confirm=True)
                t.save()
            user.coin = coin
            user.save()
            return Response("Sửa thông tin thành công")
        except Exception:
            return Response(data="Sửa đổi thông tin thất bại", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "POST":
        try:
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()
            return Response("Tạo User Thành Công")
        except Exception:
            return Response("Tạo User Thất Bại. Vui lòng thử lại", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Phương thức không hợp lệ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@ permission_classes([permissions.IsAdminUser])
@authentication_classes([JWTAuthentication])
def DeleteUser(request):
    try:
        user = User.objects.get(id=int(request.POST.get("id", "")))
        user.delete()
        return Response("Xóa Người Dùng Thành Công")
    except Exception:
        return Response("Xóa Người Dùng Thất Bại", status=status.HTTP_400_BAD_REQUEST)


class TransactionListAdmin(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        queryset = TransactionUser.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = TransactionUserSerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)


class SearchUser(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        query = request.GET["query"]
        if query:
            queryset = User.objects.filter(Q(email__icontains=query) | Q(
                coin__icontains=query) | Q(date_joined__icontains=query))
        else:
            queryset = User.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = UserSerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)


class SearchTransaction(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        query = request.GET["query"]
        if query:
            queryset = TransactionUser.objects.filter(Q(users__email__icontains=query) | Q(description__icontains=query) | Q(
                option__icontains=query) | Q(money__icontains=query) | Q(created_at__icontains=query))
        else:
            queryset = TransactionUser.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = TransactionUserSerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
