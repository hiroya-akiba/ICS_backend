from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view()),
    path('products/<int:id>/', views.ProductView.as_view()),
    path('purchase/', views.PurchaseView.as_view()),
    path('sales/', views.SalesView.as_view()),
    # ModelViewSet
    # 参照系->get, 登録系->post
    path('products/model/', views.ProductModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    
]