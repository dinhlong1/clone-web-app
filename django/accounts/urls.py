from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('accounts', views.AccountsList, basename="Accounts")
router.register('categories', views.CategoryListAdmin, basename="Categories")
router.register('account/search', views.SearchAccount,
                basename="SearchAccount")
router.register('category/search', views.SearchCategory,
                basename="SearchCategory")

urlpatterns = [
    path('store/', views.CategoryList.as_view()),
    path('account/id=<int:id>', views.AccountDetail.as_view()),
    path('account/', csrf_exempt(views.AccountViews)),
    path('account/delete/', csrf_exempt(views.DeleteAccount)),
    path('category/', csrf_exempt(views.CategoryViews)),
    path('category/id=<int:id>', views.CategoryDetail.as_view()),
    path('category/delete/', csrf_exempt(views.DeleteCategory)),
    path('', include(router.urls)),
]
