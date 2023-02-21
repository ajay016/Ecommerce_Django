var updateBtns = document.getElementsByClassName("update-cart")

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(e){
        e.preventDefault();

        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('ProductId:', productId, 'action:', action)

        console.log('User: ', user)
 
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action){
    console.log("Not logged in...")

    if(action == "add"){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        // If the quantity is equal or less than 0 remove the item
        if(cart[productId]['quantity'] <= 0){
            console.log('Item Removed')
            // Remove the item from the cart
            delete cart[productId]
        }
    }

    if(action == 'delete'){
        delete cart[productId]
    }
    

    console.log('Cart:', cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })
    .then((data) =>{
         
        console.log('data:', data)
        console.log('each_item_quantity:', data.each_item_quantity)
        
        //location.reload();

        // If the server sends the data successfully, anad if the quantity = 0 or the action is remove, it will remove the product from the list in the cart

        if (data.success){    
            console.log('data:', data)
            var dynamicProductId = 'quantity-input-field' + data.productId
            console.log('product_id:', data.productId)
            var quantityInputId = document.getElementById(dynamicProductId)
            
            document.getElementById("cart-total").innerHTML = data.order
            quantityInputId.value = data.each_item_quantity

            // Checks if it is the cart page
            // if(window.location.href.includes('cart')){

            let cartItemValue = document.getElementById("cart-item-value")

            cartItemValue.innerText = 'Cart (' + data.order + ' ' + (data.order === 1 ? 'item' : 'items') + ')'

            // If the quantity is equal to 0 remove the item
                // Remove Item in the cart page if the 'Remove Item' button is clicked           
            if(data.action == 'delete' || quantityInputId.value == 0){
                
                var productDivId = 'cart-product-' + data.productId
                var productDiv = document.getElementById(productDivId)
                console.log('Removing item from cart')
                productDiv.remove()
                // let productDiv = removeCartBtn.parentNode
                console.log('productDiv:', productDiv)                  
            }             
            // }

            // Checks if it is the product detail page
            // if(window.location.href.includes('product_detail')){

            //     // disable the '-' and '+' buttons if the quantity is less than 1
            //     // If the quantity is equal or less than 0 remove the item
            //     if(quantityInputId.value == 1){

            //         // the querySelector finds a button with the class "data-product that has 'data-product == productID' and then removes it from the DOM"
            //         let removeBtn = document.querySelector(`button[data-product='${data.productId}'][data-action='remove']`);
            //         removeBtn.classList.add('quantity-btn-disabled');

            //     }
            //     if(quantityInputId.value > 1){
            //         let removeBtn = document.querySelector(`button[data-product='${data.productId}'][data-action='remove']`);
            //         removeBtn.classList.remove('quantity-btn-disabled');

            //     }
            // }
                            
        }
        else{
            console.error('Error updating cart item:')
        }
    })
}