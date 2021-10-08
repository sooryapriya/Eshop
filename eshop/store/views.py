from math import floor
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect
from.models.customer import Customer
from.models.sample import Sample
from.models.product import Product
from.models.category import Category
from.models.orders import Orders


def index(request):
    basket = request.session.get('basket')
    if not basket:
        request.session.cart = {}
    samples = Sample.get_all_sample()
    info = {}
    info['samples'] = samples
    for s in samples:
        s.afterpercent = s.rate - (s.rate * s.percent / 100)
        s.afterpercent = floor(s.afterpercent)
    return render(request, 'store/index.html', info)


def ValidateCustomer(customer):
    error_message = None
    if not customer.name:
        error_message = "Name required!"
    elif len(customer.password) < 6 or len(customer.password) > 6:
        error_message = "Please provide a  6 char long password !"
    elif len(customer.mobnumber) < 10 or len(customer.mobnumber) > 10:
        error_message = "Please provide a valid Mobile number required!"
    elif not customer.state:
        error_message = "Please select a valid state!"
    elif not customer.city:
        error_message = "City Required!"
    elif len(customer.zip) < 6:
        error_message = "Please enter a valid Zip!"
    elif customer.isExists():
        error_message = 'Email Address Already Registered!'
    return error_message


def registeruser(request):
    postData = request.POST
    name = postData.get('name')
    email = postData.get('email')
    password = postData.get('password')
    mobnumber = postData.get('mobnumber')
    state = postData.get('state')
    city = postData.get('city')
    zip = postData.get('zip')
    # validation

    value = {'name': name,
             'email': email,
             'password': password,
             'mobnumber': mobnumber,
             'state': state,
             'city': city,
             'zip': zip
            }
    error_message = None
    customer = Customer(name=name, email=email, password=password, mobnumber=mobnumber,
                                state=state, city=city, zip=zip)
    error_message = ValidateCustomer(customer)
    if not error_message:
        customer.password = make_password(customer.password)
        # print(name, email, password, mobnumber, state, city, zip)
        customer.register()
        return render(request, 'store/login.html')
        #return HttpResponse("Account Created..")
    else:
        data = {
            'error': error_message,
            'values': value
            }
        return render(request, 'store/signup.html', data)
        # return render(request, 'signup.html', {'error': error_message})
        #print(name, email, password, mobnumber, state, city, zip)
        #return HttpResponse(request.POST.get('email'))


class Signup(View):
    def get(self, request):
        return render(request, 'store/signup.html')

    def post(self, request):
        return registeruser(request)


class Login(View):
    def get(self, request):
        return render(request, 'store/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['customer_name'] = customer.name
                request.session['email'] = customer.email
                return redirect('products')
                # return HttpResponse("login success")
            else:
                error_message = "Email or password Incorrect!"
        else:
            error_message = "Email or password Incorrect!"
        print(customer)
        print(email, password)
        return render(request, 'store/login.html', {'error': error_message})


def empty(request):
    return render(request, 'store/empty.html')


def emptycart(request):
    return render(request, 'store/emptycart.html')


def logout(request):
    request.session.clear()
    return redirect('home')


class Base(View):
    def post(self, request):
        product = request.POST.get('product')
        removefromcart = request.POST.get('removefromcart')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if removefromcart:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        #print(request.session.get('cart'))
        print(product)
        return redirect('products')


    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        categories = Category.get_all_categories()
        catid = request.GET.get('category')
        if catid:
            products = Product.get_all_products_by_id(catid)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        print(request.session.get('customer_name'))
        for i in products:
            i.afterdiscount = i.price - (i.price * i.discount / 100)
            print(i.afterdiscount)
            i.afterdiscount = floor(i.afterdiscount)
        return render(request, 'store/product.html', data)
        # print(pdt)
        # return render(request, 'order/orders.html')
        # return render(request, 'index.html', {'products': pdt})


class Cart(View):
    def get(self,request):
        if request.session.get('cart'):
            ids = list(request.session.get('cart').keys())
            products = Product.get_products_by_id(ids)
            print(products)
            return render(request, 'store/cart.html', {'products': products})
        else:
            return render(request,'store/emptycart.html')

    def post(self, request):
        product = request.POST.get('product')
        removefromcart = request.POST.get('removefromcart')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if removefromcart:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        #print(request.session.get('cart'))
        #print(product)
        return redirect('cart')


def order(request):
    return render(request, 'store/order_placed.html')


class CheckOut(View):
    def get(self, request):
        if request.session.get('cart'):
            ids = list(request.session.get('cart').keys())
            products = Product.get_products_by_id(ids)
            print(products)
            return render(request, 'store/checkout.html', {'products': products})

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobnumber = request.POST.get('mobnumber')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(name, email, mobnumber, address, state, city, zip, customer)
        for prod in products:
            prod.afterdiscount = prod.price - (prod.price * prod.discount / 100)
            prod.afterdiscount = floor(prod.afterdiscount)
            orders = Orders(customer=Customer(id=customer),
                            product=prod,
                            quantity=cart.get(str(prod.id)),
                            price=prod.afterdiscount,
                            name=name,
                            email=email,
                            mobnumber=mobnumber,
                            address=address,
                            city=city,
                            state=state,
                            zip=zip
                            )
            orders.save()
        request.session['cart']= {}
            #print(orders.place_order())

        return render(request, 'store/success.html')


def success(request):
    return render(request, 'store/success.html')
# Create your views here.


class Order(View):
    def get(self, request):
        customer = request.session.get('customer')
        order = Orders.get_orders_by_customer(customer)
        print(order)
        return render(request, 'store/order_placed.html', {'order': order})

    def post(self, request):
        return redirect('home')