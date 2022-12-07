from django.shortcuts import render,redirect
from .models import Buyer,Cart
from seller.models import Product
import random
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay

# Create your views here.

def index(request):
    all_product=Product.objects.all()
    try:
        user_object = Buyer.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'user_object': user_object,'all_product':all_product})
    except:
        return render(request, 'index.html',{'all_product':all_product})

def about(request):
    return render(request,'about.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['re_password']:
            try:
                user_email = Buyer.objects.get(email = request.POST['email'] )
                return render(request, 'register.html', {'message': 'Email already exists!!'})
            except:
                global user_dict
                user_dict = {
                    'first_name' : request.POST['first_name'],
                    'last_name' : request.POST['last_name'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'password' : request.POST['password'],
                }
                subject = 'Registration!!!'
                global generated_otp
                generated_otp = random.randint(100000, 999999)
                message = f'Your OTP is {generated_otp}.'
                from_email = settings.EMAIL_HOST_USER
                list1 = [request.POST['email']]
                send_mail(subject, message, from_email, list1)
                return render(request, 'otp.html', {'message': 'check your MailBox!!!'})
        else:
            return render(request, 'register.html', {'message': 'Both passwords are not same'})

def otp(request):
    if request.method == 'POST':
        if generated_otp == int(request.POST['otp']):
            Buyer.objects.create(
                first_name = user_dict['first_name'],
                last_name = user_dict['last_name'],
                email = user_dict['email'],
                mobile = user_dict['mobile'],
                password = user_dict['password']
            )
            return render(request, 'login.html', {'message': 'Account created successfully!!'})
        else:
            return render(request, 'otp.html', {'message': 'OTP Does not Match!!'})
    else:
        return render(request, 'login.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            session_user = Buyer.objects.get(email = request.POST['email'])
            if request.POST['password'] == session_user.password:
                request.session['email'] = session_user.email
                return redirect('index')
            else:
                return render(request, 'login.html', {'message': 'Wrong Password!!'})
        except:
            return render(request, 'login.html', {'message': 'User with this Email does not exist.'})

        
def logout(request):
    del request.session['email']
    return redirect('index')


def edit_profile(request):
    if request.method=='GET':
        try:
            user_object=Buyer.objects.get(email=request.session['email'])
            return render(request,'edit_profile.html',{'user_object':user_object})
        except:
            return render(request,'login.html')
        
    else:
        user_object=Buyer.objects.get(email = request.session['email'])
        user_object.first_name = request.POST['first_name']
        user_object.last_name=request.POST['last_name']
        user_object.email=request.POST['email']
        user_object.mobile=request.POST['mobile']
        user_object.password=request.POST['password']
        user_object.gender=request.POST['gender']
        user_object.dob=request.POST['dob']
        if request.FILES:
            user_object.pic = request.FILES['pic']
        user_object.save()
        return redirect('index')
        
def checkout(request):
    user_object=Buyer.objects.get(email=request.session['email'])
    cart_product=Cart.objects.filter(buyer=user_object)
    return render(request,'cart.html',{'user_object':user_object,'cart_product':cart_product})

def delect_cart_product(request,pk):
    del_onject=Cart.objects.get(id=pk)
    del_onject.delete()
    user_object=Buyer.objects.get(email=request.session['email'])
    cart_product=Cart.objects.filter(buyer=user_object)
    return render(request,'cart.html',{'user_object':user_object,'cart_product':cart_product})
    
    
def add_to_cart(request, pk):
    try:
        Cart.objects.create(
            product = Product.objects.get(id = pk),
            buyer = Buyer.objects.get(email = request.session['email']),
            quantity = request.GET[str(pk)]
        )
        return redirect('index')
    except KeyError:
        return render(request, 'login.html')
    except:
        return render(request, '500.html')
    


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def make_payment(request):

    user_object = Buyer.objects.get(email = request.session['email'])

    
    #updating quantity from cart page
    # session_cart_products = Cart.objects.filter(buyer = user_object)
    # for single_item in session_cart_products: 
    #     single_item.quantity = request.POST[str(single_item.id)]
    #     single_item.save()

    #calculating total price to pay
    cart_product = Cart.objects.filter(buyer = user_object)
    total_price = 0
    for item in cart_product:
        total_price += item.product.price * item.quantity


    #razorpay stuff
    currency = 'INR'
    global amount
    amount = total_price * 100 
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['cart_product'] = cart_product
    context['total_price'] = total_price
    return render(request, 'payment.html', context=context )
    
    
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            
            global amount
            amount = amount  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                session_user = Buyer.objects.get(email = request.session['email'])
                cart_product =  Cart.objects.filter(buyer = session_user)
                for i in cart_product:
                    i.delete()
                # render success page on successful caputre of payment
                return render(request, 'success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
            
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()