from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('product_order/', views.productOrder, name='product_order'),
    path('process_order/', views.processOrder, name='process_order'),
    path('cookie_order/', views.cookieOrder, name='cookie_order'),
    path('product_detail/<int:id>/', views.productDetail, name='product_detail'),
]
