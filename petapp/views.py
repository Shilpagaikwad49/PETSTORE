from django.shortcuts import render,redirect
from petapp.models import Pet,Cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail

# Create your views here.

def homefunction(request):
    context = {}
    data = Pet.objects.all()
    context['pets'] = data
    return render(request,'index.html',context)

def searchPetByType(request,val):
    context = {}
    data = Pet.objects.filter(type = val )
    context['pets'] = data
    return render(request,'index.html',context)

def sortPetsByPrice(request,dir):
    col=''
    context ={}
    if dir =='asc':
       col ='price'
    else:
        col='-price'
    data =Pet.objects.all().order_by(col)
    context ['pets'] =data
    return render(request,'index.html',context)
        
def rangeofprice(request):  
    context = {}
    min = request.GET['min']
    max = request.GET['max']
    c1 = Q(price__gte = min )
    c2 = Q(price__lte = max )
    data = Pet.objects.filter(c1 & c2)
    context ['pets'] = data
    return render(request,'index.html', context )
    
        
def petdetails(request,pid):
    context = {}
    data = Pet.objects.filter(id=pid)
    context['pet'] = data[0]
    return render(request,'petdetails.html',context)

def userlogin(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        context={}
        n= request.POST['username']
        p= request.POST['password']
        if n=='' or p=='':
            context['error']= 'please enter all the fields !!!'
            return render(request,'register.html',context)
        else:
            user = authenticate(username=n,password=p)
            if user is not None:
                login(request,user)
                # messages.success(request,'Successfully Logged In!!!')
                return redirect('/')
            else:
                context['error']= 'please provide correct details'
                return render(request,'login.html',context)
                      
            
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        context ={}
        n= request.POST['username']
        e= request.POST['email']
        p= request.POST['password']
        cp= request.POST['confirmpass']
        if n=='' or e =='' or p=='' or cp=='':
            context['error']= 'please enter all the fields !!!'
            return render(request,'register.html',context)
        elif p !=cp:
            context['error']= 'password and confirm password must be same'
            return render(request,'register.html',context)
        else:
            user =User.objects.create(username = n,email = e)
            user.set_password(p) # to set encrepted password
            user.save()
            context['success'] ='Registered Successfully !! please login'
            return render(request,'login.html',context)
        
def userlogout(request):
    context={}
    context['success'] ='Logged out successfully !! '
    logout(request)
    return redirect('/')  
        
def addtocart(request,petid):
    userid=request.user.id
    if userid is None:
        context ={}
        context['error'] = 'please login so as to add the pet in yur cart'
        return render(request,'login.html',context) 
    else:
        userid=request.user.id
        users =User.objects.filter(id=userid)
        pets =Pet.objects.filter(id=petid)
        cart =Cart.objects.create(pid =pets[0], uid = users[0])
        cart.save()
        messages.success =(request,'Pet added to cart !!')
    return redirect('/')

def showMyCart(request):
    context={}
    userid=request.user.id
    data=Cart.objects.filter(uid=userid)
    context['mycart']=data
    count= len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'mycart.html',context)

def removeCart(request,cartid):
    data = Cart.objects.filter(id = cartid)
    data.delete()
    # messages.success(request ,"Pet removed from your cart")
    return redirect('/mycart')

def confirmorder(request):
    context={}
    userid=request.user.id
    data=Cart.objects.filter(uid=userid)
    context['mycart']=data
    count= len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'confirmorder.html',context)

def makepayment(request):
    context={}
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    client =razorpay.Client(auth=('rzp_test_mqwWgS01dKEopt','6uwlOt3K7ull4I8YnOLjBaiO'))   
    data = {"amount":total*100,"currency": "INR","receipt":""}
    payment =client.order.create(data=data)
    print(payment)
    context['data'] = payment
    return render (request,'pay.html',context)
 
    
def placeorder(request):
    userid=request.user.id
    user=User.objects.filter(id=userid)
    mycart=Cart.objects.filter(uid=userid)
    ordid=random.randrange(10000,99999)
    # 23452
    for cart in mycart:
        pet=Pet.objects.filter(id=cart.pid.id) #fetching pet objects as wee need to set objects references
        ord=Order.objects.create(uid=user[0],pid=pet[0],quantity=cart.quantity,orderid=ordid)
        ord.save()
    mycart.delete()
    
    msg_body='order id is :'+str(ordid)
    custEmail=request.user.email
    send_mail(
    "order place successfully",       #subject
    msg_body,
    "shilpagaikwad2000@gmail.com",  #from
    [custEmail],                         #to
    fail_silently=False,
    )  
    
    # messages.success(request,"Order placed Succesfully!!!")
    return redirect('/')

def updateQuantity(request,cartId,operation):
    data =Cart.objects.filter(id = cartId)
    cart = data[0]
    if operation == 'sub':
        data.update(quantity = cart.quantity - 1)
    else:
        data.update(quantity = cart.quantity + 1)    
    return redirect('/mycart')


def demo_fn():
    return 'welcome'
