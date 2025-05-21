import datetime
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *

# Store page
def store(request):
    category = request.GET.get('category')
    query = request.GET.get('search')
    search_query = request.GET.get('search-query')
    products = Product.objects.all()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
        
    if category:
        products = products.filter(category__icontains=category)

    if search_query:
        products = products.filter(name__icontains=search_query)
    
    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except:
            pass
        
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'products': products, 'cartItems': cartItems, 'search-query': search_query}
    return render(request, 'store/store.html', context)

# Cart page
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # Create empty cart for non-logged-in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

# Checkout page
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items            
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data.get('quantity', 1)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

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
                phone=data['shipping']['phone'],
            )
    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)

def after_checkout(request):
    if request.method == "POST":
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')

        order.name = name
        order.email = email
        order.address = address
        order.city = city
        order.state = state
        order.phone = phone
        order.complete = True
        order.save()

        new_order = Order.objects.create(customer=customer, complete=False)
        OrderItem.objects.filter(order=order).delete()

        return render(request, 'store/after_checkout.html', {
            'name': name,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'phone': phone
        })
    else:
        return redirect('store')

def reset_cart(request):
    if 'cart' in request.session:
        del request.session['cart']


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def filter_products(request):
    # Lọc theo loại
    category = request.GET.get('category', '')
    # Lọc theo giá
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 999999)

    # Lọc sản phẩm
    products = Product.objects.all()
    
    if category:
        products = products.filter(category__icontains=category)
    
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    
    return render(request, 'store/product_list.html', {'products': products})