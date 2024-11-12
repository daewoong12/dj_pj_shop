"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path, include
app_name='mall'
urlpatterns = [
    path('', views.product_list, name='product_list'),  # 제품 목록
    path('', views.product_list, name='index'),  # index URL도 함께 참조 가능
    path('<int:stuff_id>/', views.detail, name='detail'),
    path('register/', views.register_stuff, name='register_stuff'),
    path('info/', views.info, name='info'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:stuff_id>/add', views.addCart, name='addcart'),
    path('cart/<int:stuff_id>/delete', views.subCart, name='subCart'),
    path('cart/<int:stuff_id>/plus', views.plusStuff, name='plusStuff'),
    path('cart/<int:stuff_id>/minus', views.minusStuff, name='minusStuff'),
    path('buy/<int:stuff_id>/', views.buyAtIndex, name='buyAtIndex'),
    path('buy/', views.buy, name='buy'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('add_to_cart/<int:stuff_id>/', views.add_to_cart, name='add_to_cart'),
    path('<int:stuff_id>/update/', views.update_stuff, name='update_stuff'),  # 상품 수정
    path('<int:stuff_id>/delete/', views.delete_stuff, name='delete_stuff'),  # 상품 삭제
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
]
