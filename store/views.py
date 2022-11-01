from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *

def store(request):
    
    products = Product.objects.all()
    
    # check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # if the user is authenticated assign the user to a customer
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            
            # showing the item quantity in the cart icon, not an efficient way to do it
            cartItems = order.get_cart_items
            
        except:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            
    # if the user is not authenticated the cart item shows 0
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        
        # cartItems shows the item quantity in the cart icon, not an efficient way to do it
        cartItems = order['get_cart_items']
        
    # cartItems shows the item quantity in the cart icon, not an efficient way to do it
    context = {'products': products, 'order': order, 'cartItems': cartItems}
    # context = {'products': products, 'order': order}
    return render(request, 'store/store.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
        # showing the item quantity in the cart icon, not an efficient way to do it
        cartItems = order.get_cart_items
        
        # my code
        # shows the total number of items in the cart
        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        
        # cartItems shows the item quantity in the cart icon, not an efficient way to do it
        cartItems = order['get_cart_items', 'shipping': False]
        
    # cartItems shows the item quantity in the cart icon, not an efficient way to do it
    context = {'items': items, 'order': order, 'cartItems': cartItems}    
    
    # context = {'items': items, 'order': order}
    return render(request, 'store/cart1.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
        # showing the item quantity in the cart icon, not an efficient way to do it
        cartItems = order.get_cart_items
        
        # my code
        # shows the total number of items in the cart
        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        
        # cartItems shows the item quantity in the cart icon, not an efficient way to do it
        cartItems = order['get_cart_items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    
    # the request is from 'cart.js' fetch url, data is the value mof the json response from the 'cart.js'
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('ProductId:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    # clicking on the 'Add to Cart' button will increase the quantity by 1 if the item is already
    # in the cart, if not the item will be added
    if action == 'add':
        orderItem.quantity += 1
        orderItem.save()
        
    elif action == 'remove':
        orderItem.quantity -= 1
        orderItem.save()
    
        
    elif action == 'delete':
        orderItem.delete()
        
    # orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

