import json
from .models import *

def cookieCart(request):
    
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
        # Try to get the product by its "id". If it is removed return empty cart
        try:
            # 'cart[i]["quantity"]' returns the quantity of the product
            # we get the quantity from the cookie set in the javascript and called here by 'cart = json.loads(request.COOKIES['cart'])'
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
            
            # render the items for unauthenticated user to display in the cart page
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
    
    return {'items': items, 'order': order, 'cartItems': cartItems}

def cartData(request):
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
        try:
            customer = request.user.customer
        except :
            customer = {}
        
    print('Customer:', customer)
    return {'items': items, 'order': order, 'cartItems': cartItems, 'customer': customer}

def guestOrder(request, data):
    
    # From this line to the for loop 'for item in items' can be put inside the 'processOrder' function in views.py file
    print('User is not logged in...')
        
    # For unauthenticated user get the user information from the form that the customer has to fill during checkout
    print(f'Cookies:{request.COOKIES}')
    first_name = data['form']['first_name']
    last_name = data['form']['last_name']
    email = data['form']['email']
    phone = data['form']['phone']
    
    # Get the cookie data from util.py
    cookieData = cookieCart(request)
    # 'cookieData' returns dictionary where 'items' is one of the keys
    items = cookieData['items']
    
    # Create a customer with his email if he is not registered. We get this email from the checkout form and is passed here in json format by using javascript in 'checkout.html' file
    customer, created = Customer.objects.get_or_create(email=email, first_name=first_name)
    # Cusomer may want to change his email. This is why we write this code outside the 'get_or_create' method
    # customer.first_name = first_name
    customer.last_name = last_name
    customer.phone = phone
    customer.save()
    
    # Create order
    # Both authenticated and unauthenticated user need to have order and orderItems
    order = Order.objects.create(
        customer = customer,
        complete = False
    )
    
    for item in items:
        # Get the product by its id
        product = Product.objects.get(id=item['product']['id'])
        
        # Create OrderItem in the database for the products
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    
    return customer, order