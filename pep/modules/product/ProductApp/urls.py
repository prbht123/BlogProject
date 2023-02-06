from django.urls import path
from modules.product.ProductApp import views

app_name = "ProductApp"

urlpatterns = [
    path('home/', views.Home, name='home'),
    path('create/', views.ProductCreate.as_view(), name="productcreate"),
    path('update/<int:pk>/', views.ProductUpdate.as_view(), name="productupdate"),
    path('detail/<int:pk>/', views.ProductDetail.as_view(), name="productdetail"),
    path('delete/<int:pk>/', views.ProductDelete.as_view(), name="productdelete"),
    path('list/', views.ProductList.as_view(), name="productlist"),
    path('order/<int:pk>', views.OrderCreate.as_view(), name="ordercreate"),
    path('order_done/', views.order_done, name="order_done"),
    path('orderlist/', views.OrderList.as_view(), name="orderlist"),
    path('orderdetail/<int:pk>/', views.OrderDetail.as_view(), name="orderdetail"),
    path('cartlist/', views.CartList.as_view(), name="cartlist"),
    path('addcart/<int:pk>', views.addcart, name="addcart"),
    path('removecart/<int:pk>', views.removecart, name="removecart"),
    path('ordercart/<int:pk>/', views.OrderCart.as_view(), name="ordercart"),
    path('updatecart/<int:pk>/', views.AddCartUpdate.as_view(), name="updatecart"),
    path('payment/<int:pk>/', views.PaymentOrder, name='payment'),
    path('paymentcart/<int:pk>/', views.PaymentCart, name='paymentcart'),
    path('paymentstatus/<int:pk>/', views.PaymentStatus, name = 'paymentstatus')
]
