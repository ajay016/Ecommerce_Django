from django.shortcuts import render
from django.http import JsonResponse
import datetime
import json
from .models import *
from .utils import cookieCart

def store(request):
    
    products = Product.objects.all()
    
    # check if the user is authenticated
    # if the user is authenticated, return the no. of item in the acrt and the cart total
    # else return empty cart and a cart  total of 0
    if request.user.is_authenticated:
        # try:
        # if the user is authenticated, assign the user to a customer
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
        # showing the item quantity in the cart icon, not an efficient way to do it
        cartItems = order.get_cart_items
            
        # except:
    else:
        # items = []
        # order = {'get_cart_total': 0, 'get_cart_items': 0}
        # cartItems = order['get_cart_items']
        cookieData = cookieCart(request)
        order = cookieData['order']
        cartItems = cookieData['cartItems']
        
            
    # if the user is not authenticated the cart item shows 0
    # else:
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        
    #     # cartItems shows the item quantity in the cart icon, not an efficient way to do it
    #     cartItems = order['get_cart_items']
        
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
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
        
    # cartItems shows the item quantity in the cart icon, not an efficient way to do it
    context = {'items': items, 'order': order, 'cartItems': cartItems}    
    #print('Items:', items)
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
        # if the user is unauthenticated return empty cart items and order
        # items = []
        # customer = {}
        # order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        
        # cartItems shows the item quantity in the cart icon, not an efficient way to do it
        # cartItems = order['get_cart_items']
        
        # if the user is unauthenticated return the items, order and cartItems from the cookie that we got through javascript in utils.py file
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer}
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

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
            
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zip_code=data['shipping']['zipcode']
            )
            
            print('data: ', data)
    else:
        print('User is not logged in...')
    
    return JsonResponse('Payment Complte', safe=False)

