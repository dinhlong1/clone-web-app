import requests
from rest_framework.response import Response
from rest_framework import generics
from .models import Category, Account
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from .serializers import CategorySerializer, AccountSerializer, CategorySerializerAdmin
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
from django.utils import timezone
from django.core.signing import Signer
from django.core.management.utils import get_random_secret_key  


def check_live(uid):
    url = "https://graph.facebook.com/{}/picture?type=normal".format(uid)
    response = requests.get(url)
    if "//static" in response.url:
        return False
    else:
        return True


class CategoryList(generics.RetrieveAPIView):
    def get(self, request):
        categorys = Category.objects.all()
        
        print(get_random_secret_key())
        serializer = CategorySerializer(categorys, many=True)
        return Response(data=serializer.data)


class AccountsList(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        queryset = Account.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = AccountSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class AccountDetail(APIView):
    @ permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def get(self, request, id, format=None):
        try:
            account = Account.objects.filter(id=id)
            serializer = AccountSerializer(account, many=True)
            return Response(data=serializer.data)
        except Exception:
            return Response("Tài khoản không tồn tại", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAdminUser])
def AccountViews(request):
    if request.method == 'POST':
        try:
            data = request.POST.get("data", "")
            category = int(request.POST.get("category", ""))
            parameter = request.POST.get("params", "").split(',')

            list_account = data.split("\n")
            for i in range(len(list_account)):
                account = (list_account[i].replace(" ", "")).split("|")
                a = Account.objects.create(category_id=category)
                if "uid" in parameter:
                    index = int(parameter.index("uid"))
                    print(check_live(account[index]))
                    if check_live(account[index]) != True or account[index] == "" or Account.objects.filter(uid=account[index]).exists() == True:

                        a.delete()
                        continue
                    a.uid = account[index]
                else:
                    a.delete()
                    continue
                if "password" in parameter:
                    index = parameter.index("password")
                    a.password = account[index]
                else:
                    a.delete()
                    continue
                if "auth" in parameter:
                    index = parameter.index("auth")
                    a.auth = account[index]
                if "email" in parameter:
                    index = parameter.index("email")
                    a.email = account[index]
                if "password_email" in parameter:
                    index = parameter.index("password_email")
                    a.password_email = account[index]
                if "token" in parameter:
                    index = parameter.index("token")
                    a.password_email = account[index]
                if "cookie" in parameter:
                    index = parameter.index("cookie")
                    a.password_email = account[index]
                a.updated_at = timezone.now()
                a.save()
            return Response("Tạo Thành Công", status=status.HTTP_200_OK)
        except Exception:
            return Response("Thêm Thất bại", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        try:
            password = request.data["password"]
            auth = request.data["auth"]
            email = request.data["email"]
            password_email = request.data["password_email"]
            token = request.data["token"]
            cookie = request.data["cookie"]
            sold = request.data.get("sold", "")
            live = request.data.get("status", "")
            account = Account.objects.get(id=int(request.data.get("id", "")))
            account.password = password
            if auth == "null" or auth == "":
                account.auth = None
            else:
                account.auth = auth
            if email == "null" or email == "":
                account.email = None
            else:
                account.email = email
            if password_email == "null" or password_email == "":
                account.password_email = None
            else:
                account.password_email = password_email
            if token == "null" or token == "":
                account.token = None
            else:
                account.token = token
            if cookie == "null" or cookie == "":
                account.cookie = None
            else:
                account.cookie = cookie

            account.status = live
            account.sold = sold
            account.updated_at = timezone.now()
            account.save()
            return Response("Sửa thông tin thành công")
        except Exception:
            return Response("Sửa đổi thông tin tài khoản thất bại", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Phương thức không hợp lệ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@ permission_classes([permissions.IsAdminUser])
@authentication_classes([JWTAuthentication])
def DeleteAccount(request):
    try:
        account = Account.objects.get(id=int(request.POST.get("id", "")))
        account.delete()
        return Response("Xóa Tài Khoản Thành Công")
    except Exception:
        return Response("Xóa Tài Khoản Thất Bại", status=status.HTTP_400_BAD_REQUEST)


class SearchAccount(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        query = request.GET["query"]
        if query:
            queryset = Account.objects.filter(Q(uid__icontains=query) | Q(password__icontains=query) | Q(auth__icontains=query) | Q(
                email__icontains=query) | Q(password_email__icontains=query) | Q(cookie__icontains=query) | Q(token__icontains=query))

        else:
            queryset = Account.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = AccountSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# Category
class CategoryListAdmin(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        queryset = Category.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = CategorySerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)


class CategoryDetail(APIView):
    @ permission_classes([permissions.IsAdminUser])
    @authentication_classes([JWTAuthentication])
    def get(self, request, id, format=None):
        try:
            category = Category.objects.filter(id=id)
            serializer = CategorySerializer(category, many=True)
            return Response(data=serializer.data)
        except Exception:
            return Response("Tài khoản không tồn tại", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
@permission_classes([permissions.IsAdminUser])
@authentication_classes([JWTAuthentication])
def CategoryViews(request):
    if request.method == "PUT":
        try:
            name = request.POST["name"]
            price = request.POST["price"]
            discount = request.POST["discount"]
            category = Category.objects.get(id=int(request.POST.get("id", "")))
            category.name = name
            category.price = price
            category.discount = discount
            category.updated_at = timezone.now()
            category.save()
            return Response("Sửa thông tin thành công")
        except Exception:
            return Response(data="Sửa đổi thông tin thất bại", status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "POST":
        try:
            name = request.POST.get("name", "")
            price = int(request.POST.get("price", ""))
            discount = int(request.POST.get("discount", ""))
            a = Category.objects.create(
                name=name, price=price, discount=discount)
            a.updated_at = timezone.now()
            a.save()
            return Response("Thêm Dữ Liệu Thành Công")
        except Exception:
            return Response("Thêm Dữ Liệu Thất Bại", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Phương thức không hợp lệ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@ permission_classes([permissions.IsAdminUser])
@authentication_classes([JWTAuthentication])
def DeleteCategory(request):
    try:
        account = Category.objects.get(id=int(request.POST.get("id", "")))
        account.delete()
        return Response("Xóa Loại Tài Khoản Thành Công")
    except Exception:
        return Response("Xóa Loại Tài Khoản Thất Bại", status=status.HTTP_400_BAD_REQUEST)


class SearchCategory(viewsets.GenericViewSet):
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([JWTAuthentication])
    def list(self, request):
        query = request.GET["query"]
        if query:
            queryset = Category.objects.filter(Q(name__icontains=query) | Q(price__icontains=query) | Q(
                discount__icontains=query) | Q(quantity__icontains=query) | Q(created_at__icontains=query))
            print(queryset)
        else:
            queryset = Category.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = CategorySerializerAdmin(page, many=True)
        return self.get_paginated_response(serializer.data)
