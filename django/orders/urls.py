from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('history-transaction', views.TransactionsList,
                basename="Transactions")
router.register('history', views.OrdersList, basename="Orders")
router.register('order/order-detail',
                views.OrdersDetailListAdmin, basename="OrderDetail")
router.register('orders', views.OrdersListAdmin, basename="Orders")
router.register('order/search', views.SearchOrder, basename="SearchOrder")


urlpatterns = [
    path('payment/', csrf_exempt(views.payment)),
    path('history/detail/', csrf_exempt(views.ShowDetail)),
    path('dashboard/', csrf_exempt(views.DashBoardViews)),
    # path('order/order-detail/id=<int:id>/', views.OrdersDetailListAdmin.as_view()),
    path('', include(router.urls))
]
