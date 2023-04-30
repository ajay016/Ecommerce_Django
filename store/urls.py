from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product_detail/<int:id>/', views.productDetail, name='product_detail'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('update_profile/', views.updateProfile, name='update_profile'),
    path('signup_form/', views.signup_form, name='signup_form'),
    path('update_item/', views.updateItem, name='update_item'),
    path('product_order/', views.productOrder, name='product_order'),
    path('process_order/', views.processOrder, name='process_order'),
    path('cookie_order/', views.cookieOrder, name='cookie_order'),
]
