from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Cart,SubCategories,Categories,Wishlist,Address,Orders
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,"index.html",context)

def product_details(request,pid):
    products = Product.objects.get(id= pid)
    date = datetime.datetime.today().date() + datetime.timedelta(days=5)
    context = {'products':products,'date':date}
    return render(request,"product_details.html",context)

def signup(request):
    if request.method == "POST":
       uname = request.POST['uname']
       fname = request.POST['fname']
       lname = request.POST['lname']
       email = request.POST['email']
       pass1 = request.POST['pass1']
       pass2 = request.POST['pass2']

       if pass1 == pass2:
           user = User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=pass1)
           user.save()
           return redirect('signin')
       else:
           error = "password and confirm password does not match"
           context={'error':error}
           return render(request,"signup.html",context)
       
    else: 
        error = "invalid request"
        context={'error':error}
        return render(request,"signup.html",context)

def signin(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST['password']
        user = authenticate(username=uname,password=password)
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            error ="username or password does not match"
            context={'error':error}
            return render(request,"signin.html",context)
            
    return render(request,"signin.html")


def signout(request):
    logout(request)
    return redirect('index')


def add_cart(request,pid):
    product = Product.objects.get(id=pid)
    user = request.user if request.user.is_authenticated else None
    if user:
        cart_item ,created = Cart.objects.get_or_create(product=product,user=user)
    else:
        return redirect('signin')
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity=1
    
    cart_item.save()
    return redirect('index')


def cart(request):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user = request.user)
    else:
        cart_item = Cart.objects.filter(user = None)
    
    

    total_price=0

    for x in cart_item:
        total_price += (x.product.price * x.quantity)

    length = len(cart_item)
    context ={'items':cart_item,'total':total_price,'total_product':length}
    return render(request,"cart.html",context)


def updateqty(request,val,pid):
    c = Cart.objects.filter(product = pid , user = request.user)
    if val == 0:
        if c[0].quantity>1:
            a = c[0].quantity-1
            c.update(quantity=a)
    else:
        a = c[0].quantity+1
        c.update(quantity=a)
    return redirect('cart')


def remove_product(request,pid):
    c = Cart.objects.filter(product = pid , user = request.user)
    c.delete()
    return redirect('cart')


def add_wishlist(request,pid):
    product = Product.objects.get(id=pid)
    user = request.user if request.user.is_authenticated else None
    if user:
         wishlist_item , created = Wishlist.objects.get_or_create(product = product,user = user)
    else:
        return redirect('signin')
    
    if not created:
        error="already added to wishlist"
    else:
        wishlist_item.save()
    return redirect('wishlist')

def wishlist(request):
    if request.user.is_authenticated:
        wishlist_item = Wishlist.objects.filter(user = request.user)
    else:
        wishlist_item = Wishlist.objects.filter(user = request.user)

    context = {}
    context['items']= wishlist_item
    return render(request,"wishlist.html",context)

def remove_wishlist(request,pid):
    wishlist_item = Wishlist.objects.filter(user = request.user,product=pid)
    wishlist_item.delete()
    return redirect('wishlist')

def address(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            new_address = request.POST['address']
            new_pincode = request.POST['pincode']
            total_addresses = Address.objects.filter(user = request.user)
            if len(total_addresses) < 3:
                add_address = Address.objects.create(user=request.user,address=new_address,pincode=new_pincode)
                add_address.save()
                return redirect('address')
            else:
                address = Address.objects.filter(user = request.user)
                return render(request,"address.html",{'address':address})
        else:
            address = Address.objects.filter(user = request.user)
            return render(request,"address.html",{'address':address})
    else:
        return redirect('signin')
    
def delete_address(request,id):
    if request.user.is_authenticated:
        address = Address.objects.filter(user=request.user,id=id)
        address.delete()
        return redirect('address')
    
def update_address(request,id):
    if request.user.is_authenticated:
        address = Address.objects.filter(user=request.user)
        update_address = get_object_or_404(Address,user=request.user,id = id)
        if request.method =="POST":
            update_address.address=request.POST.get('address')
            update_address.pincode=request.POST.get('pincode')
            update_address.save()
            return redirect('address')
        else:
            return render(request,"address.html",{'update_address':update_address,'address':address})
    else:
        return redirect('signin')


def confirm_order(request,id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
        address = Address.objects.get(id=id,user=request.user)
    else:
        return redirect('signin')
    context = {}
    context['items']= cart_item
    context['address'] = address
    list=[]
    total_price = 0
    for x in cart_item:
        total_price += (x.product.price * x.quantity)
        list.append(total_price)
    
    context['list']=list
    context['total']=total_price
    length = len(cart_item)
    context['total_product']=length

    return render(request,"confirm_order.html",context)

import random
import razorpay

def payment(request,id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
        address = Address.objects.get(id=id,user=request.user)
        order_id =0
        total_price = 0
        for x in cart_item:
            total_price += (x.product.price * x.quantity)
            order_id = random.randrange(1000,9999)
            date = datetime.datetime.today().date()
            Orders.objects.create(order_id=order_id,product=x.product,user = request.user,order_date=date,address=address,quantity=x.quantity)
            x.delete()
        client = razorpay.Client(auth=("rzp_test_n0lhpmrEfeIhGJ","UOrbXQGnsEc2dhB1IFg0zNWZ"))
        data = {"amount":total_price*100,"currency":"INR","receipt":str(order_id)}
        payment= client.order.create(data=data)

        context ={"data":data,"amount":payment,"payment_status":False}

        return render(request,"payment.html",context)
    else:
        return redirect('signin')


def orders(request):
    if request.user.is_authenticated:
        allorders  = Orders.objects.filter(user = request.user)
    return render(request,"orders.html",{'allorders':allorders})


