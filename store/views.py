from django.shortcuts import render
from django.http import JsonResponse
import datetime
import json
from .models import *
from .utils import cookieCart, cartData, guestOrder

def store(request):
    
    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems']
    
    products = Product.objects.all()

    main_categories = MainCategory.objects.all()
    a = MainCategory.objects.get(id=1)
    flash_sale_products = Product.objects.filter(flash_sale=True)
    print('flash sale: ', flash_sale_products)
    
    # check if the user is authenticated
    # if the user is authenticated, return the no. of item in the acrt and the cart total
    # else return empty cart and a cart  total of 0
    # if request.user.is_authenticated:
    #     # try:
    #     # if the user is authenticated, assign the user to a customer
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
        
    #     # showing the item quantity in the cart icon, not an efficient way to do it
    #     cartItems = order.get_cart_items
            
    #     # except:
    # else:
    #     # items = []
    #     # order = {'get_cart_total': 0, 'get_cart_items': 0}
    #     # cartItems = order['get_cart_items']
    #     cookieData = cookieCart(request)
    #     order = cookieData['order']
    #     cartItems = cookieData['cartItems']
        
            
    # if the user is not authenticated the cart item shows 0
    # else:
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        
    #     # cartItems shows the item quantity in the cart icon, not an efficient way to do it
    #     cartItems = order['get_cart_items']
        
    # cartItems shows the item quantity in the cart icon, not an efficient way to do it
    context = {'products': products, 'order': order, 'cartItems': cartItems, 'main_categories': main_categories}
    # context = {'products': products, 'order': order}
    return render(request, 'store/store.html', context)


def cart(request):
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    p = []
    
    # for p in items:
    #     print('Items:', p.product.price)
        
    # cartItems shows the item quantity in the cart icon, not an efficient way to do it
    context = {'items': items, 'order': order, 'cartItems': cartItems}    
    # print('Items:', items)
    
    # for i in items:
    #     p.append(i.product)

    # print(p)
    # context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def productDetail(request, id):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    product = Product.objects.get(id=id)
    
    print('items:', items)
    product_quantity = 1
    # for i in items:
    #     if i.product.id == product.id:
    #         product_quantity = i.quantity
    # print('product_quantity:', product_quantity)

    # print(product.id)
    
    context = {
        'product': product,
        'cartItems': cartItems,
        'items': items,
        'order': order,
        'product_quantity': product_quantity
        }
    
    return render(request, 'store/product.html', context)


def checkout(request):
            
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    customer = data['customer']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    
    # the request is from 'cart.js' fetch url, data is the value of the json response from the 'cart.js'
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
         
    if orderItem.quantity <= 0:
        orderItem.delete()


    cart_quantity = order.get_cart_items
    each_item_quantity = orderItem.quantity

    # return JsonResponse('Item was added', safe=False)
    return JsonResponse({'success':True, 'order': cart_quantity, 'each_item_quantity': each_item_quantity, 'productId': productId, 'action': action})


def productOrder(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']

    print('Action:', action)
    print('ProductId:', productId)
    print('quantity:', quantity)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'productAdd':
        orderItem.quantity += quantity
        orderItem.save()

    cart_quantity = order.get_cart_items
    each_item_quantity = orderItem.quantity

    # once the data is sent to frontend and the quantity is updated in the database, the quantity in the input field will be reset to 1
    reset_quantity = 1


    return JsonResponse({'success':True, 'order': cart_quantity, 'each_item_quantity': each_item_quantity,
                         'productId': productId, 'action': action, 'quantity': quantity, 'reset_quantity': reset_quantity})



def cookieOrder(request):
    cookie_data = cookieCart(request)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    items = cookie_data['items']
    order = cookie_data['order']
    cartItems = cookie_data['cartItems']
    cart = []

    if cart == items:
        each_item_quantity = 0

    try:
        for product_quantity in items:
            if int(product_quantity['product']['id']) == int(productId):
                print(product_quantity['product']['id'])
                each_item_quantity = product_quantity['quantity']
                print(True)
                break
            else:
                each_item_quantity = 0
                print('Else:', False)
    except:
        each_item_quantity = 0
        print('except:', each_item_quantity)
            
    # print('ProductId: ', productId)
    print('Cokkie order:', items)
    print('cookie: ', cookie_data)
    print('action: ', action)
    print('each_item_quantity:', each_item_quantity)
    # print('productId: ', items['product']['id'])
    # print(each_item_quantity)

    return JsonResponse({'success':True, 'items': items, 'order': order, 'cartItems': cartItems, 'productId': productId, 'action': action, 'each_item_quantity': each_item_quantity})


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        # 'guestOreder' function returns customer and order. The function has been created in utils.py file 
        customer, order = guestOrder(request, data)
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    print(total == float(order.get_cart_total))
    if total == float(order.get_cart_total):
        print(total == float(order.get_cart_total))
        order.complete = True
        
    order.save()
    print('Complete:', order.complete)
    print('Customer:', customer.first_name)
    print('Customer:', customer.email)
    print('Customer:', customer.phone)
    
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
        
    return JsonResponse('Payment Complete', safe=False)
