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
    
    return {'items': items, 'order': order, 'cartItems': cartItems}