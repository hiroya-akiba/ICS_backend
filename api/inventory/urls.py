from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('products/', views.ProductView.as_view()),
    path('products/<int:id>/', views.ProductView.as_view()),
    path('purchase/', views.PurchaseView.as_view()),
    path('purchase/<int:id>/', views.PurchaseView.as_view()),
    path('sales/', views.SalesView.as_view()),
    path('sales/<int:id>/', views.SalesView.as_view()),
    path('inventories/<int:id>/', views.InventoryView.as_view()),
    # ModelViewSet
    # 参照系->get, 登録系->post
    path('products/model/', views.ProductModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view()),
]