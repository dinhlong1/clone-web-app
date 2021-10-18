from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt

from . import views

router = DefaultRouter()
router.register('user/list', views.UserList, basename="User")
router.register('transactions', views.TransactionListAdmin,
                basename="Transactions")
router.register('user/search', views.SearchUser, basename="SearchUser")
router.register('transaction/search', views.SearchTransaction,
                basename="SearchTransaction")
urlpatterns = [
    path('account/', views.MyProfile.as_view()),
    path('obtain_token/',  views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView().as_view(), name='token_get_access'),
    path('user/', csrf_exempt(views.UserViews)),
    path('user/id=<int:id>', views.UserDetail.as_view()),
    path('user/delete/', csrf_exempt(views.DeleteUser)),
    path('', include(router.urls)),
]
