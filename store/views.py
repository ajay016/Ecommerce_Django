from django.shortcuts import render
from django.http import JsonResponse
import datetime
import json
from .models import *

def store(request):
    
    products = Product.objects.all()
    
    # check if the user is authenticated
    # if the user is authenticated, return the no. of item in the acrt and the cart total
    # else return empty cart and a cart  total of 0
    if request.user.is_authenticated:
        try:
            # if the user is authenticated, assign the user to a customer
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            
            # showing the item quantity in the cart icon, not an efficient way to do it
            cartItems = order.get_cart_items
            
        except:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
            
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
        # if the user is not authenticated
        # get the cookies from the website. The name of the cookie was 'cart'
        # All the cookies is in json format. Convert it in python dictionary using json.loads
        # Get all the cookies using 'request.cookies['cart]', here name of the cookie is '[cart]'
        try:
            cart = json.loads(request.COOKIES['cart'])
            print('Cart:', cart)
        except:
            cart = {}
            
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0 , 'shipping': False}
        
        # cartItems shows the item quantity in the cart icon, not an efficient way to do it
        cartItems = order['get_cart_items']
        
        # loop through the cart dictionary, cart contains "2: '{quantity: 1}'", where '2' is the productID
        # and '{quantity: 1}' is dictionary within the cart dictionary containig the quantity of the product
        for i in cart:
            # Try to get the product by its "id", if it is removed return empty cart
            try:
                # 'cart[i]["quantity"]' returns the quantity of the product
                # we get the quantity of the from the cookie set in the javascript and called here by 'cart = json.loads(request.COOKIES['cart'])'
                # So, for an unauthenticated user quantitiy of products in the cart is zero as set in the "order"
                # "cartItems" which was "0" to the value of the quantity that we got from the cookie
                cartItems += cart[i]["quantity"]
                
                # Get the product id from the cookie
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]["quantity"])
                
                # Get the total amount of the cart
                order['get_cart_total'] += total
                
                # Get the total number of items in the cart
                order['get_cart_items'] += cart[i]["quantity"]
                
                # render the items for unauthenticated user to display n the cart page
                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL
                    },
                    'quantity': cart[i]["quantity"],
                    'get_total': total
                }
                
                items.append(item)
                
                #print('Order:', order)
                if product.digital == False:
                    order['shipping'] = True
            
            except:
                pass
        
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
        items = []
        customer = {}
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        
        # cartItems shows the item quantity in the cart icon, not an efficient way to do it
        cartItems = order['get_cart_items']
        
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

