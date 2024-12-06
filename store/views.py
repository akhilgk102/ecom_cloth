from django.shortcuts import render,redirect
from django.views.generic import View
from store.forms import SignUpForm,SignInForm,OrderForm

from django.core.mail import send_mail
from store.models import User,Size,BasketItem,OrderItem,Order

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.db.models import Sum,F,Count
# Create your views here.

from django.shortcuts import HttpResponse
from django.utils.timezone import now

from store.models import Product
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decouple import config


RZP_KEY_ID=config('RZP_KEY_ID')

RZP_KEY_SECRET=config('RZP_KEY_SECRET')


def send_otp_phone(otp):

    from twilio.rest import Client
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='+15635546540',
    body=f"Your OTP is: {otp}",
    to='+917736668179',
    )
    print(message.sid)


def send_otp_email(user):

    user.generate_otp()

    send_otp_phone(user.otp)

    subject="Verify E-mail Address"

    message=f"OTP for Account Verification is {user.otp}"

    from_email="akhilgkrishnan102@gmail.com"

    to_email=[user.email]

    send_mail(subject,message,from_email,to_email)


    

class SignUpView(View):

    template_name="register.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            user_object=form_instance.save(commit=False)

            user_object.is_active=False

            user_object.save()

            send_otp_email(user_object)

            messages.success(request,"OTP Has been sent to you E-mail and Phone.")

            return redirect("verify-email")

        return render(request,self.template_name,{"form":form_instance})


class SignInView(View):
    template_name="login.html"
    form_class=SignInForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{'form':form_instance})
    

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                messages.success(request,"Loggined Successfully")

                return redirect("index")

        return render(request,self.template_name,{'form':form_instance})

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        messages.success(request,"Sign Out Successfully")

        return redirect("signin")


class VerifyEmailView(View):

    template_name="verify_email.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):

        otp=request.POST.get("otp")

        try:
            
                user_object=User.objects.get(otp=otp)

                user_object.is_active=True

                user_object.is_verified=True

                user_object.otp=None

                user_object.save()

                messages.success(request,"Your OTP is Verified.")

                return redirect("signin")

        except:

            messages.error(request, "Invalid OTP. Please try again.")

            return render(request, self.template_name)


class ProductListView(View):

    template_name="index.html"
    
    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        paginator=Paginator(qs,6)

        page_number=request.GET.get("page")

        page_obj=paginator.get_page(page_number)

        return render(request,self.template_name,{"page_obj":page_obj,"books":qs})

    """
    Current Page Number : ?page={{page_obj.number}}

    Next Page Number: ?page={{page_obj.next_page_number}}

    Previous Page Number : ?page={{page_obj.previous_page_number}}

    Last Page Number : ?page={{page_obj.paginator.num_pages}}
        
    """
    

class ProductDetailView(View):
    template_name="product_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Product.objects.get(id=id)
        
        return render(request,self.template_name,{"product":qs})
    
    # def post(self,request,*args,**kwargs):



class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        size=request.POST.get("size")

        quantity=request.POST.get("quantity")

        product_object=Product.objects.get(id=id)

        size_object=Size.objects.get(name=size)

        basket_obj=request.user.cart

        BasketItem.objects.create(
            product_object=product_object,
            quantity=quantity,
            size_object=size_object,
            basket_object=basket_obj

        )

        print("Item added to cart")

        


        messages.success(request,"Item Added to Cart")


        return redirect("cart-summary")
    

class CartSummaryView(View):

    template_name="cart_summary.html"


    def get(self,request,*args,**kwargs):


        qs=BasketItem.objects.filter(basket_object=request.user.cart,is_order_placed=False)

        # Total Items
        # items=qs.aggregate(total_items=Count('basket_object_id')) 

        items=qs.count()



        # Total Price

        basket_total=sum([bi.item_total for bi in qs])

        
        return render(request,self.template_name,{"basket_item":qs,"total_items":items,'basket_total':basket_total})


class CartItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")


import razorpay

class PlaceOrderView(View):

    template_name='place_order.html'

    form_class=OrderForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class

        qs=request.user.cart.cart_item.filter(is_order_placed=False)

        total=sum([bi.item_total for bi in qs])

        print(total)

        return render(request,self.template_name,{"form":form_instance,"unordered_items":qs,"total":total})
    


    
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.instance.customer=request.user

            order_instance=form_instance.save()

            basket_items=request.user.cart.cart_item.filter(is_order_placed=False)

            payment_method=form_instance.cleaned_data.get("payment_method")

            for bi in basket_items:

                OrderItem.objects.create(
                    order_object=order_instance,
                    product_object=bi.product_object,
                    quantity=bi.quantity,
                    size_object=bi.size_object,
                    price=bi.product_object.price
                )

                bi.is_order_placed=True

                bi.save()
            

            # raz_integration
            if payment_method=="ONLINE":

                client=razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))

                total=sum([ bi.item_total for bi in basket_items])*100

                data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }

                payment = client.order.create(data=data)

                rzp_order_id=payment.get("id")

                order_instance.rzp_order_id=rzp_order_id

                order_instance.save()

                context={

                    "key_id":RZP_KEY_ID,
                    "order_id":rzp_order_id,
                    "currency":"INR",
                    "amount":total

                }

                return render(request,"payment.html",context)



        return redirect("index")
    


class OrderSummaryView(View):

    template_name="order_summary.html"

    def get(self,request,*args,**kwargs):

        qs=request.user.orders.all().order_by("-created_date")

        return render(request,self.template_name,{"orders":qs})





class OrderDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Order.objects.get(id=id).delete()

        return redirect("order-summary")




@method_decorator([csrf_exempt],name="dispatch")
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))

        try:


            client.utility.verify_payment_signature(request.POST)
            print("payment success")

            order_id=request.POST.get("razorpay_order_id")

            order_object=Order.objects.get(rzp_order_id=order_id)

            order_object.is_paid=True

            order_object.save()

            login(request,order_object.customer)


        except:

            print("payment failed")

        return redirect("order-summary")