from datetime import datetime
from decimal import Decimal
import json
from django.core.exceptions import ValidationError
import math
import uuid
from datetime import datetime, timedelta
from django import template
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
import httpx
from main import models as main_models
from django.http import Http404, HttpResponse, JsonResponse
from .models import SalerDetail, Product, ProductSize, SellerSlider, MyCart, WholeSaleProduct, category, Orders, WholeSaleProductOrders
from django.contrib import messages
from django.contrib.auth.models import User,Group
from .forms import SalerRegisterForm, SalerAddressForm, UpdateSalerDetailForm, UpdateSalerAccountDetailForm
from main.forms import UserUpdateForm, UpdateUserDetailForm,UpdateStudentProfileForm
from django.contrib.auth.decorators import login_required
from math import ceil
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from . import forms
from channels.db import database_sync_to_async
from . import models
from asgiref.sync import sync_to_async
from django.db.models import Count
from django.contrib import auth
from django.db.models import Q
from django.core.serializers import serialize
from room import models as room_models
# This is view of Index Page of Seller in which we Display Whole Sale Products


@login_required
def index(request):
    context={
        
    }
    
    return render(request, 'saler/index.html', context)
    
# This is View of Dashboard in which we display all orders of the seller and ther status


@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'GET':
            odrr = request.GET.get('odrr')
            st = request.GET.get('st')
            if st == 'Cancel':
                o = Orders.objects.filter(order_id=odrr).first()
                o.status = 'Cancel'
                o.save()
            if st == 'Accepted':
                o = Orders.objects.filter(order_id=odrr).first()
                o.status = 'Accepted'
                o.save()
            # if st == 'Packed':
            # 	o = Orders.objects.filter(order_id=odrr).first()
            # 	o.status = 'Packed'
            # 	o.save()
            if st == 'Delivered':
                o = Orders.objects.filter(order_id=odrr).first()
                o.status = 'Delivered'
                o.save()
        ordr = [i for i in Orders.objects.filter(
            saler=request.user) if i.status != 'Cancel' and i.status != 'On The Way' and i.status != 'Delivered'][::-1]
        params = {
            'orders': ordr,
            'dorders': [i for i in Orders.objects.filter(saler=request.user) if i.status != 'Cancel' and i.status == 'On The Way' or i.status == 'Delivered'][::-1],
            'cart_element_no': len([p for p in MyCart.objects.all() if p.user == request.user]),
        }
        return render(request, 'saler/dashboard.html', params)
    else:
        return redirect("/")

# This is add to cart view of Seller means Whole Sale Products


@login_required
def add_to_cart(request):
    cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
    card_prods_id = [i.product_id for i in cart_prods]
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        if prod_id in card_prods_id:
            cart_prods[card_prods_id.index(
                prod_id)].number += WholeSaleProduct.objects.filter(product_id=prod_id)[0].min_Quantity
            cart_prods[card_prods_id.index(prod_id)].save()
            return HttpResponse(len(cart_prods))

        else:
            MyCart(user=request.user, product_id=prod_id, number=WholeSaleProduct.objects.filter(
                product_id=prod_id)[0].min_Quantity).save()
            return HttpResponse(len(cart_prods)+1)
    else:
        return HttpResponse("")

# This is view for Increasing Quantity of any Product in Cart


@login_required
def plus_element_cart(request):
    cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
    card_prods_id = [i.product_id for i in cart_prods]
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        if prod_id in card_prods_id:
            cart_prods[card_prods_id.index(
                prod_id)].number += WholeSaleProduct.objects.filter(product_id=prod_id)[0].min_Quantity
            cart_prods[card_prods_id.index(prod_id)].save()
            subtotal = 0.0
            delev = 0.0
            cart_prods2 = [p for p in MyCart.objects.all()
                           if p.user == request.user]
            for p in cart_prods2:
                subtotal += p.number * \
                    WholeSaleProduct.objects.filter(
                        product_id=p.product_id)[0].price
            tax = subtotal*5/100
            datas = {
                'num': MyCart.objects.filter(user=request.user, product_id=prod_id)[0].number,
                'tax': tax,
                'subtotal': subtotal,
                'delev': delev,
                'total': subtotal+tax+delev,
            }
            return JsonResponse(datas)
    else:
        return HttpResponse("")

# This is view for Decreasing Quantity of any Product in Cart


@login_required
def minus_element_cart(request):
    cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
    card_prods_id = [i.product_id for i in cart_prods]
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        if prod_id in card_prods_id:
            cart_prods[card_prods_id.index(
                prod_id)].number -= WholeSaleProduct.objects.filter(product_id=prod_id)[0].min_Quantity
            cart_prods[card_prods_id.index(prod_id)].save()
            subtotal = 0.0
            delev = 0.0
            cart_prods2 = [p for p in MyCart.objects.all()
                           if p.user == request.user]
            for p in cart_prods2:
                subtotal += p.number * \
                    WholeSaleProduct.objects.filter(
                        product_id=p.product_id)[0].price
            tax = subtotal*5/100
            datas = {
                'num': MyCart.objects.filter(user=request.user, product_id=prod_id)[0].number,
                'tax': tax,
                'subtotal': subtotal,
                'delev': delev,
                'total': subtotal+tax+delev,
            }
            return JsonResponse(datas)
    else:
        return HttpResponse("")

# This is view for Deleting a Product from Cart


@login_required
def delete_from_cart(request):
    cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
    card_prods_id = [i.product_id for i in cart_prods]
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        if prod_id in card_prods_id:
            cart_prods[card_prods_id.index(prod_id)].delete()
            subtotal = 0.0
            delev = 0.0
            cart_prods2 = [p for p in MyCart.objects.all()
                           if p.user == request.user]
            for p in cart_prods2:
                subtotal += p.number * \
                    WholeSaleProduct.objects.filter(
                        product_id=p.product_id)[0].price
            tax = subtotal*5/100
            datas = {
                'len': len(cart_prods2),
                'tax': tax,
                'subtotal': subtotal,
                'delev': delev,
                'total': subtotal+tax+delev,
            }
            return JsonResponse(datas)
    else:
        return HttpResponse("")

# This view for Display a Single Product


@login_required
def productView(request, prod_id):
    if request.user.is_superuser or request.user.is_staff:
        params = {
            'product': WholeSaleProduct.objects.filter(product_id=prod_id)[0],
            'cart_element_no': len([p for p in MyCart.objects.all() if p.user == request.user]),
        }
        return render(request, 'saler/productview.html', params)
    else:
        return redirect("/")

# This is View of Display all Products of a perticular category


@login_required
def view_all(request, catg):
    if request.user.is_superuser or request.user.is_staff:
        params = {
            'product': [i for i in WholeSaleProduct.objects.all() if str(i.category) == catg],
            'catg': catg,
            'cart_element_no': len([p for p in MyCart.objects.all() if p.user == request.user]),
        }
        return render(request, 'saler/view_all.html', params)
    else:
        return redirect("/")

# seller cart view


@login_required
def mycart(request):
    if request.user.is_superuser or request.user.is_staff:
        allProds = []
        subtotal = 0.0
        delev = 0.0
        cart_prods = [p for p in MyCart.objects.all() if p.user ==
                      request.user]
        for p in cart_prods:
            subtotal += p.number * \
                WholeSaleProduct.objects.filter(
                    product_id=p.product_id)[0].price
        tax = subtotal*5/100

        for cprod in cart_prods:
            prod = WholeSaleProduct.objects.filter(
                product_id=cprod.product_id)[0]
            allProds.append([cprod, prod])
        params = {
            'allProds': allProds,
            'cart_element_no': len([p for p in MyCart.objects.all() if p.user == request.user]),
            'total': subtotal+tax+delev,
            'subtotal': subtotal,
            'tax': tax,
            'delev': delev,
        }
        return render(request, 'saler/cart.html', params)
    else:
        return redirect("/")

# seller checkout view means for whole sale products


def checkout(request):
    if request.user.is_superuser or request.user.is_staff:
        allProds = []
        cart_prods = [p for p in MyCart.objects.all() if p.user ==
                      request.user]
        for cprod in cart_prods:
            prod = WholeSaleProduct.objects.filter(
                product_id=cprod.product_id)[0]
            allProds.append([cprod, prod])
        if request.method == 'POST':
            address_form = SalerAddressForm(
                request.POST, instance=request.user.salerdetail)
            if address_form.is_valid():
                address_form.save()
                for item in cart_prods:
                    if WholeSaleProductOrders.objects.all().last():
                        order_id = 'WSPOrder' + \
                            str((WholeSaleProductOrders.objects.all().last().pk)+1)
                    else:
                        order_id = 'WSPOrder001'
                    product1 = item.product_id+'|'+str(item.number)+','
                    WholeSaleProductOrders(
                        order_id=order_id, user=request.user, products=product1).save()
                    item.delete()
                return redirect('seller_orders')
        else:
            address_form = SalerAddressForm(instance=request.user.salerdetail)

        subtotal = 0.0
        delev = 0.0
        for p in cart_prods:
            subtotal += p.number * \
                WholeSaleProduct.objects.filter(
                    product_id=p.product_id)[0].price
        tax = subtotal*5/100
        params = {
            'allProds': allProds,
            'cart_element_no': len(cart_prods),
            'address_form': address_form,
            'total': subtotal+tax+delev,
        }
        return render(request, 'saler/checkout.html', params)
    else:
        return redirect("/")

# Orders of Seller (Whole sale product)


def MyOrders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        o = WholeSaleProductOrders.objects.filter(order_id=order_id)[0]
        o.status = 'Cancel'
        o.save()
    params = {
        'orders': [i for i in WholeSaleProductOrders.objects.all() if i.user == request.user and i.status != 'Delivered' and i.status != 'Cancel'],
        'delivered': [i for i in WholeSaleProductOrders.objects.all() if i.user == request.user and i.status == 'Delivered'],
        'cancel': [i for i in WholeSaleProductOrders.objects.all() if i.user == request.user and i.status == 'Cancel'],

    }
    return render(request, 'saler/myorders.html', params)

# for adding a new product by seller


@login_required
def add_product(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            prod_name = request.POST.get('prod_name')

            prod_seller = request.POST.get('prod_seller')
            desc = request.POST.get('desc')
            cat = request.POST.get('category')
            subcategory = request.POST.get('subcategory')
            price = request.POST.get('price')
            # price_not = request.POST.get('price_not')
            gst_l = request.POST.get('gst')
            if Product.objects.all():
                prod_id2 = 'pr'+hex(Product.objects.all().last().product_id+1)
            else:
                prod_id2 = 'pr'+hex(0)
            image1 = request.FILES.get("image1")
            image2 = request.FILES.get("image2")
            image3 = request.FILES.get("image3")
            image4 = request.FILES.get("image4")
            image5 = request.FILES.get("image5")
            size_no = int(request.POST.get('size_no'))
            i = 1
            sizes = []
            while i <= size_no:
                if request.POST.get(f'size{i}'):
                    sizes.append([request.POST.get(f'size{i}'), int(
                        request.POST.get(f'quantity{i}'))])
                i += 1
            Product(product_id2=prod_id2, shop=request.user, product_name=prod_name, prod_seller=prod_seller, category=category.objects.get(
                id=int(cat)), subcategory=subcategory, price=price, desc=desc, gst=gst_l, image1=image1).save()
            p = Product.objects.filter(product_id2=prod_id2)[0]
            if image2:
                p.image2 = image2
            if image3:
                p.image3 = image3
            if image4:
                p.image4 = image4
            if image5:
                p.image5 = image5
            p.save()
            for siz in sizes:
                ProductSize(product=p, size=siz[0], quantity=siz[1]).save()
            messages.success(request, f'Product Added !')
        prod = [p for p in Product.objects.all() if p.shop == request.user]

        if request.method == 'GET':
            pro_id = request.GET.get('pro_id', 0)
            del_prod = [p.product_id for p in Product.objects.all()
                        if p.shop == request.user]
            if int(pro_id) in del_prod:
                Product.objects.filter(product_id=int(pro_id))[0].delete()
                messages.success(
                    request, f'The Product of id {pro_id} is deleted !')
                return redirect('/tutor/add_product/')

        subcat = []
        for cat in category.objects.all():
            x = cat.sub_Categories.split(',')
            x.insert(0, cat)
            subcat.append(x)
        params = {
            'prod': prod[::-1][0:20],
            'cart_element_no': len([p for p in MyCart.objects.all() if p.user == request.user]),
            'subcat': subcat,
        }
        return render(request, 'saler/add_product.html', params)
    else:
        return redirect("/")

# it will display all products of a seller


@login_required
def view_products(request):
    if request.user.is_superuser or request.user.is_staff:
        prod = [p for p in Product.objects.all() if p.shop == request.user]

        if request.method == 'GET':
            pro_id = request.GET.get('pro_id')
            if pro_id:
                del_prod = [p.product_id for p in Product.objects.all()
                            if p.shop == request.user]
                if int(pro_id) in del_prod:
                    Product.objects.filter(product_id=int(pro_id))[0].delete()
                    messages.success(
                        request, f'The Product of id {pro_id} is deleted !')
                    return redirect('/tutor/view_products/')

        params = {
            'prod': prod[::-1],
            'cart_element_no': len([p for p in MyCart.objects.all() if p.user == request.user]),
        }
        return render(request, 'saler/view_products.html', params)
    else:
        return redirect("/")

# Signup for Seller

def tutorSignUp(request):
    if request.user.is_authenticated:
        user=request.user
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'tutor' in user_groups:
            return redirect("saler_account_settings")
        
        else:
            print(user_groups)
            return render(request, 'saler/tutor_signup.html')
       
    else:
        if request.method == "GET":
            return render(request, 'saler/tutor_signup.html')
        if request.method == 'POST':
            username = request.POST.get("username")
            email = request.POST.get("email")
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            password = request.POST.get("password")
            user_type = request.POST.get("user_type")
        
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(
                    request, 'User with this username or email already exists.')
                return render(request, 'saler/tutor_signup.html')  

            hashed_password = make_password(password)
            user = User.objects.create(
                username=username, email=email, password=hashed_password, first_name=firstname, last_name=lastname, )
            
            user.save()
            group_name = 'student' if user_type == 'student' else 'tutor'
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
            
            messages.success(request, 'Account created successfully!')
    
            usr = User.objects.filter(username=username).first()
            usr.is_staff = True
            gst = 00
            usr.save()
            if username.isdigit():
                SalerDetail(user=usr, mobile=username, gst_Number=gst).save()
            else:
                usr.email = username
                usr.save()
                SalerDetail(user=usr, gst_Number=gst).save()
            messages.success(request, f'Account is Created for {username}')
           
            return redirect('tutor_signup')

           

        
    return render(request, 'saler/tutor_signup.html')


def tutorLogin(request):

    my_variable = request.session.get('redirect_to', None)
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        # messages.success(request, f'Hi {username.title()}, welcome back!')
        user_groups = request.user.groups.values_list('name', flat=True)
        user_details = main_models.TutorUserDetails.objects.filter(user=user).first()
        
        print("User groups  ",user_groups)
        if user_details is None and 'tutor'  in user_groups:
            return redirect("updateProfile")   
        elif  user_details  and   'tutor' in user_groups:
            return redirect('saler_account_settings')
        else:
            messages.error(request, f'This Account Belongs  To a Student')
            return redirect('student_signup')
            
            
                
            # if 'tutor' in user_groups:
            #     return redirect("updateProfile")
            # else:
            #     messages.error(request, f'This Account Belongs  To a Student')
            #     return redirect('student_signup')
            
        
    messages.error(request, f'Invalid username or password')
    print("Not Authenticated")
    # url = reverse('tutor_signup') + f'?next_page={reverse("home") if referring_url is None else referring_url}'
    return redirect('tutor_signup')





# 
def student_signup(request):
    if request.user.is_authenticated:
        user=request.user
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'student' in user_groups:
            return redirect("studentProfile")
        
        else:
            
            return render(request, 'saler/student_signup.html')
       
    else:
        if request.method == "GET":
            return render(request, 'saler/student_signup.html')
        if request.method == 'POST':
            username = request.POST.get("username")
            email = request.POST.get("email")
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            password = request.POST.get("password")
            user_type = request.POST.get("user_type")
        
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(
                    request, 'User with this username or email already exists.')
                return render(request, 'saler/student_signup.html')  

            hashed_password = make_password(password)
            user = User.objects.create(
                username=username, email=email, password=hashed_password, first_name=firstname, last_name=lastname, )
            
            user.save()
            group_name = 'student' if user_type == 'student' else 'tutor'
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
            
            messages.success(request, 'Account created successfully!')
    
            usr = User.objects.filter(username=username).first()
            usr.is_staff = True
            gst = 00
            usr.save()
            if username.isdigit():
                SalerDetail(user=usr, mobile=username, gst_Number=gst).save()
            else:
                usr.email = username
                usr.save()
                SalerDetail(user=usr, gst_Number=gst).save()
            messages.success(request, f'Account is Created for {username}')
           
            return redirect('student_signup')

           

        
    return render(request, 'saler/student_signup.html')


def student_login(request):
    my_variable = request.session.get('redirect_to', None)
   
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        # messages.success(request, f'Hi {username.title()}, welcome back!')
        user_groups = request.user.groups.values_list('name', flat=True)
        user_details = main_models.StudentDetails.objects.filter(user=user).first()
     
              
        if user_details is None and 'student'  in user_groups:
            return redirect("studentProfile")   
        else:
            if my_variable is None:
                
                if 'student' in user_groups:
                    return redirect("studentProfile")
                else:
                    messages.error(request, f'This  Account  belongs to a Tutor')
                    return redirect('tutor_signup')
                    # pass
            else:
                
                return redirect(my_variable)
        
    messages.error(request, f'Invalid username or password')
    print("Not Authenticated")
   
    return redirect('student_signup')








# Seller Account Settings



def account_settings(request):
    user=request.user
    current_user=User.objects.get(id=user.id)
    saler_finances=models.TutorFinanceAccount.objects.filter(Q(last_deposit__booking__skill__tutor=user.id) | Q(last_deposit__course__tutor=user.id)).first()
    
    withdrawal_history = models.WithdrawFunds.objects.filter(account__last_deposit__booking__skill__tutor=user)
    skills = models.Skill.objects.filter(tutor=user)
    rooms = room_models.Room.objects.filter(tutor = request.user).annotate(message_count=Count('messages'))
    transactions = models.BookingPayments.objects.filter(booking__skill__tutor=user).order_by("-id")
    courses = models.Course.objects.filter(tutor=user).count()
    
    context={
        "saler_finances":saler_finances,
        "skills":skills,
        "withdrawals":withdrawal_history,
        "rooms":rooms,
        "transactions":transactions,
        "courses":courses
    }
    return render(request, 'saler/admin/home.html',context)

def studentDashboard(request):
    user=request.user
    sessions = models.TutorSession.objects.filter(payments__booking__student=user)
   
    rooms = room_models.Room.objects.filter(student=user).annotate(message_count=Count('messages'))
    
    for item in sessions:
        decimal_hours = Decimal(item.payments.booking.duration)
        total_seconds = float(decimal_hours) * 3600
        duration_timedelta = timedelta(seconds=total_seconds)
        hours, remainder = divmod(duration_timedelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        time =''
        if hours > 0:
            time =  f"{hours} hours and {minutes} minutes"
        else:
            time = f"{minutes} minutes"
        
        item.payments.booking.duration=time
    context={
        "sessions":sessions,
        "rooms":rooms
    }
    return render(request,"saler/student/student_home.html",context)


def studentBookings(request):
    
    
    student_id=request.user.id
    bookings = models.Booking.objects.filter(student=student_id).order_by("-id")
    courses = models.Course.objects.filter(customers=request.user)
 
    for item in bookings:
        decimal_hours = Decimal(item.duration)
        total_seconds = float(decimal_hours) * 3600
        duration_timedelta = timedelta(seconds=total_seconds)
        
        hours, remainder = divmod(duration_timedelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        time =''

        if hours > 0:
            time =  f"{hours} hours and {minutes} minutes"
        else:
            time = f"{minutes} minutes"
        
        item.duration=time
            

    context={
        "bookings":bookings
    }
    return render(request,"saler/student/student_bookings.html",context)


def studentCourses(request):
    courses = models.Course.objects.filter(customers=request.user)
    form = forms.CourseRatingForm()
    
    context = {
        "courses":courses,
        "form":form
    }
    
    return render(request,"saler/student/student_courses.html",context)

def studentProfile(request):
    print("Hello")
    form = UpdateStudentProfileForm()
    student_form=forms.StudentUserDetails()
    try:
       
        # user_details= get_object_or_404(main_models.UserDetail,user=request.user.id)
        user_details= get_object_or_404(main_models.StudentDetails,user=request.user.id)
        decimal_hours = Decimal(user_details.duration_per_session)
        total_seconds = float(decimal_hours) * 3600
        duration_timedelta = timedelta(seconds=total_seconds)
        
        hours, remainder = divmod(duration_timedelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        time =''

        if hours > 0:
            time =  f"{hours} hours and {minutes} minutes"
        else:
            time = f"{minutes} minutes"
        
        print("Duration is ", time)
        
        user_details.duration_per_session=time
        
        
        return render(request, "saler/student/student_profile.html", {'user_details': user_details})
    except Http404:
        # print("Not ")
        return render(request, "saler/student/student_profile.html",)

def updateStudentProfile(request):
    # form = UpdateStudentProfileForm()
    my_variable = request.session.get('redirect_to', None)
    
    print(my_variable)
    form=forms.StudentUserDetails()
    print(request.method)
    if request.method == "POST":
        contact_number = request.POST.get('contact_number')
        subjects = request.POST.get('subjects')
        grade_level = request.POST.get('grade_level')
        preferred_tutoring_format = request.POST.get('preferred_tutoring_format')
        availability = request.POST.get('availability')
        duration_per_session = request.POST.get('duration_per_session')
        budget_range = request.POST.get('budget_range')
        payment_method = request.POST.get('payment_method')
        languages_preference = request.POST.get('languages_preference')
        qualifications_desired = request.POST.get('qualifications_desired')
        accept_terms = request.POST.get('accept_terms')== "on"
        privacy_preference = request.POST.get('privacy_preference')
        
        
        student = main_models.StudentDetails(
            contact_number=contact_number,
            subjects=subjects,
            grade_level=grade_level,
            preferred_tutoring_format=preferred_tutoring_format,
            availability=availability,
            duration_per_session=duration_per_session,
            budget_range=budget_range,
            payment_method=payment_method,
            languages_preference=languages_preference,
            qualifications_desired=qualifications_desired,
            accept_terms=accept_terms,
            privacy_preference=privacy_preference
        )
        
        student.user = request.user
        student.save()
        print("STudent Data Saved")
        print("My  Variable  is ",my_variable)
        if my_variable is not None:
            return redirect(my_variable)
        else:
            return redirect("studentProfile")
      
    else:
       return redirect("home")    
        


def updateProfile(request):
    my_variable = request.session.get('redirect_to_skill', None)
    user=request.user
    
    
    user_details= main_models.TutorUserDetails.objects.filter(user=user.id).first()
    events=main_models.Event.objects.all()
    serialized_data = serialize('json', events)
    
   
    
    
    if user_details is None:
        return updateProfileForm(request)
    else:
        if my_variable is None:
            return render(request, "saler/admin/profile.html", {'user_details': user_details,"events":events,"serialized_data":serialized_data})

        else:
                return redirect(my_variable)
 
def addAvailableDay(request):
    if request.method == "POST":
        print("DATA IS",request.POST)
        date=request.POST.get("date")
        print("Date is ",date)
        event = main_models.Event.objects.create(
            day=date,
            user=request.user
        )
        event.save()
        print("saaved")
        
        return redirect("updateProfile")
    else:
        return redirect("updateProfile")

def saveForm(request,userDetails:main_models.TutorUserDetails=None):
    my_variable = request.session.get('redirect_to', None)
    user=request.user

    contact_number = request.POST.get('contact_number')
    profile_picture = request.FILES.get('profile_picture')
    cv = request.FILES.get('cv')
    highest_qualification = request.POST.get('highest_qualification')
    specialization = request.POST.get('specialization')
    years_of_experience = request.POST.get('years_of_experience')
    teaching_style = request.POST.get('teaching_style')
    teaching_philosophy = request.POST.get('teaching_philosophy')
    availability = request.POST.getlist('availability')
    preferred_teaching_method = request.POST.get('preferred_teaching_method')
    hourly_rate = request.POST.get('hourly_rate')
    preferred_payment_method = request.POST.get('preferred_payment_method')
    education_materials_link = request.POST.get('education_materials_link')
    languages_spoken = request.POST.get('languages_spoken')
    special_certificate_skills = request.POST.get('special_certificate_skills')
    special_certificate_files = request.FILES.get('special_certificate_files')
    cancellation_policy = request.POST.get('cancellation_policy')
    terms_acceptance = request.POST.get('terms_acceptance') == "on"
   
    tutor_instance = main_models.TutorUserDetails(
        user=user,
        contact_number=contact_number,
        profile_picture=profile_picture,
        highiest_qualification=highest_qualification,
        specialization=specialization,
        years_of_experience=years_of_experience,
        teaching_style=teaching_style,
        teaching_philosophy=teaching_philosophy,
        availability=availability,
        preferred_teaching_method=preferred_teaching_method,
        hourly_rate=hourly_rate,
        preferred_payment_method=preferred_payment_method,
        education_materials_link=education_materials_link,
        languages_spoken=languages_spoken,
        special_certificate_skills=special_certificate_skills,
        special_certificate_files=special_certificate_files,
        # cancellation_policy=cancellation_policy,
        terms_acceptance=terms_acceptance,
        cv=cv
    )
    
    if 'profile_picture' not in request.FILES:
        tutor_instance.profile_picture = userDetails.profile_picture
    if 'cv' not in request.FILES:
        tutor_instance.cv=userDetails.cv    

      
       
    
    tutor_instance.save()
    
   

    # Save multiple files for special_certificate_files
    
    print("Success")
    return redirect('updateProfile')


def updateProfileForm(request):
    my_variable = request.session.get('redirect_to', None)
    user=request.user
    form = forms.TutorUserDetailsForm()
    modelInstance=main_models.TutorUserDetails()
    tutordetails = main_models.TutorUserDetails.objects.filter(user=user).first()
    
    print(request.method)
    if request.method == "POST":
        return saveForm(request,userDetails=tutordetails)
        
    else:
        tutordetails = main_models.TutorUserDetails.objects.filter(user=user).first()
        if tutordetails:
            
            return render(request,"saler/admin/updateDetailsForm.html",{"TutorUserDetails":modelInstance,"user":tutordetails})
        else:
          
            return render(request,"saler/admin/updateDetailsForm.html",{"TutorUserDetails":modelInstance,"user":tutordetails})


def deactivateProfile(request):
    
    user = request.user
   
    user_groups = request.user.groups.values_list('name', flat=True)
    
   
    if request.method == "POST":
        user = get_object_or_404(User, id=request.user.id)
        user.is_active = False
        user.save()
        return redirect("home")
    else:
        if 'student' in user_groups:
            return render(request,"saler/student/student_deactivate_profile.html")
        else:
            return render(request,"saler/admin/deactivateProfile.html")
    

def addSkill(request):
    user_details= main_models.TutorUserDetails.objects.filter(user=request.user).first()
    if user_details is None:
        request.session['redirect_to_skill'] = request.build_absolute_uri()
        
        
    page = "skills"
    try:
        form = forms.AddSkillForm()
        # Skills= get_object_or_404(models.Skill,tutor=request.user.id)
        skills = models.Skill.objects.filter(tutor = request.user.id).order_by('-id')
        # time_slots =skills.
        context = {
            "skills": skills,
            "skill_form":form
            }
        return render(request, "saler/admin/add_skill.html",context )
    except Http404:
        return addTutorSkillsForm(request)
       
    
def addTutorSkillsForm(request):
    user_details= main_models.TutorUserDetails.objects.filter(user=request.user).first()
    if user_details is None:
        request.session['redirect_to'] = request.build_absolute_uri()
        
        
    form = forms.AddSkillForm()
    context={
        "skill_form":form
    }
    if request.method == "POST":
       
        form = forms.AddSkillForm(request.POST,request.FILES)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.tutor = request.user
            skill.save()
            messages.success(request,"Profile Updated")
            print("form saved")
            return redirect("addSkill")
        else:
            print("invalid form")
            return render(request, "saler/admin/add_skill.html",context)     
    else:
       
        return render(request, "saler/admin/add_skill.html",context)  


def addTimeSlot(request,skill_id):
    page="slots"
    slots = models.TimeSlots.objects.filter(skill=skill_id)
    form=forms.AddTimeSlotForm()
    print(slots.count())
    
    
    
    try:
        form = forms.AddTimeSlotForm()
        
        slots = models.TimeSlots.objects.filter(skill = skill_id).order_by('-id')
        context={
            "slots": slots,
            "skill_id":skill_id,
            "slot_form":form}
        
        return render(request, "saler/admin/time_slots.html", context)
    except Http404:
        return addTimeSlotForm(request,skill_id=skill_id)
    
def addTimeSlotForm(request,skill_id):
    form = forms.AddTimeSlotForm(request)
   
   
    context={
        "slot_form":form
    }
   
    if request.method == "POST":
       
        form = forms.AddTimeSlotForm(request.POST,request.FILES)
        if form.is_valid():
            slot = form.save(commit=False)
            skill=models.Skill.objects.get(id=skill_id)
            slot.skill = skill
            slot.save()
            messages.success(request,"Time Slot Added")
           
            return redirect("addSkill")
        else:
            print("invalid form")
            return render(request, "saler/admin/time_slots.html",context)     
    else:
       
        return render(request, "saler/admin/time_slots.html",context)  
    
def staffBookings(request):
    tutor_id = request.user.id
    bookings = models.Booking.objects.filter(skill__tutor=tutor_id).order_by("-id")
    # booking = get_object_or_404(models.Booking, id=booking_id)
    for item in bookings:
        decimal_hours = Decimal(item.duration)
        total_seconds = float(decimal_hours) * 3600
        duration_timedelta = timedelta(seconds=total_seconds)
        
        hours, remainder = divmod(duration_timedelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        time =''

        if hours > 0:
            time =  f"{hours} hours and {minutes} minutes"
        else:
            time = f"{minutes} minutes"
        
        item.duration=time
    
    booking_form=forms.BookingStatusUpdateForm(request.POST)
    context = {
        "bookings":bookings,
        "form":booking_form
    }

    return render(request,"saler/admin/bookings.html",context)

def update_booking_status(request, booking_id):
    booking = get_object_or_404(models.Booking, id=booking_id)
    tutor_id = request.user.id
    bookings = models.Booking.objects.filter(skill__tutor=tutor_id).order_by("-id")
    
    for item in bookings:
        decimal_hours = Decimal(item.duration)
        total_seconds = float(decimal_hours) * 3600
        duration_timedelta = timedelta(seconds=total_seconds)
        
        hours, remainder = divmod(duration_timedelta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        time =''

        if hours > 0:
            time =  f"{hours} hours and {minutes} minutes"
        else:
            time = f"{minutes} minutes"
        
        item.duration=time
    # booking = get_object_or_404(models.Booking, id=booking_id)
    booking_form=forms.BookingStatusUpdateForm(request.POST)
    context = {
        "bookings":bookings,
        "form":booking_form
    }
    if request.method == 'POST':
        form = forms.BookingStatusUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            print("form saved")
            # Add any additional logic after saving the form if needed
    else:
        form = forms.BookingStatusUpdateForm(instance=booking)

    return render(request,"saler/admin/bookings.html",context)




def reviews(request):
    tutor_reviews=main_models.TutorRating.objects.all()
    
    for item in tutor_reviews:
        item.rating =range(0,item.rating)
    
    context={
        "tutor_reviews":tutor_reviews
    }
    return render(request,"saler/admin/reviews.html",context)

def logout_tutor(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('home')



def tutor_profile(request,tutor_id):
    request.session['redirect_to'] = request.build_absolute_uri()
    # print(tutor_id)
    tutor = main_models.TutorUserDetails.objects.get(user = tutor_id)
    skills = models.Skill.objects.filter(tutor=tutor_id)
    tutor_rating = main_models.TutorRating.objects.filter(tutor=tutor.user)
    form_data = request.session.pop('form_data', None)
    events = main_models.Event.objects.all()
    
    
    periods_json = request.session.get('periods', '[]')
    periods = json.loads(periods_json)
    
    
    events_data=serialize('json',events)
    # print("Date events",date_events)
    if tutor_rating.count() == 0:
        rating=0,
        average_rating=0
    else:
    
        total_rating = 0
        for item in tutor_rating:
            total_rating+=item.rating
            
        for item in tutor_rating:
            item.rating =range(0,item.rating)
        
        # if tutor_rating.count() == 0:
        
        
        average_rating = math.ceil(total_rating/tutor_rating.count())
    
        
        
        rating=range(0,average_rating)
        
        
    context={
        "tutor":tutor,
        "skills":skills,
        "rating":rating,
        "avg_rating":average_rating,
        "tutor_reviews":tutor_rating,
        "form_data":form_data,
        "events_data":events_data,
        "periods":periods
        # "date_events":date_events
    }
    return render(request,"saler/tutor_profile.html",context)

# @login_required
def bookSession(request,tutor_id):
    request.session['redirect_to'] = request.build_absolute_uri()
    user=request.user
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        message= request.POST.get("message")
        skill_id = request.POST.get("skill")
        duration = request.POST.get("duration")
        skill = models.Skill.objects.get(id=skill_id)
        end=request.POST.get("end")
        tutor=models.User.objects.get(id=tutor_id)
        request.session['form_data'] = request.POST
        
            
        events = main_models.Event.objects.filter(user=skill.tutor)
            
        try:
            start_time = datetime.strptime(time, "%H:%M").time()
            # end_time = datetime.strptime(end, "%H:%M").time()
            
            
            duration_minutes = float(duration)*60
            duration_timedelta = timedelta(minutes=duration_minutes)
            calculated_end_time = (datetime.combine(datetime.today(), start_time) + duration_timedelta).time()
            

            event = main_models.Event.objects.create(
                user=skill.tutor,
                day=date,
                start_time=start_time,
                end_time=calculated_end_time,
                notes=skill.title
            )
            event.save()
            if event.id is not None:
                
                print("Event id si ",event.id)
                session = models.Booking.objects.create(
                date=date,
                time=time,
                skill=skill,
                student=user,
                duration=duration,
                student_message=message,
                
                )
                session.save()
                print("session id is ",session.id)
                return redirect("studentBookings")
            else:
                return redirect("bookSession",tutor_id=tutor_id)  
        except ValidationError as e:
            
                messages.error(
                    request, e)
                print("Error is ",str(e))  
                return redirect("bookSession",tutor_id=tutor_id)               
       
    else:
        return redirect("studentBookings")
    
    
# def convert_date_to_string(obj):
#     if isinstance(obj, date):
#         return obj.strftime('%Y-%m-%d')
#     return obj


def checkAvailability(request,tutor_id):
    if request.method == "POST":
        tutor = models.User.objects.get(id=tutor_id)
        date=request.POST.get("date")
        
        events = main_models.Event.objects.filter(user=tutor, day=date).order_by('start_time')
        periods=[]
        for item in events:
            if item.start_time is None:
                pass
            else:
                period={
                "start_time":item.start_time.strftime('%H:%M'),
                "end_time":item.end_time.strftime('%H:%M'),
                
                }
                periods.append(period)
            
            
        periods_json = json.dumps(periods)
        request.session['periods'] = periods_json
      
     
        return redirect("tutor_profile",tutor_id=tutor_id) 
    
    else:
        return redirect("tutor_profile",tutor_id=tutor_id) 

def rateTutor(request,tutor_id):
    request.session['redirect_to'] = request.build_absolute_uri()
    if request.method == "POST":
        if request.user.is_authenticated:
            review = request.POST.get("review")
            rate = request.POST.get("rating")
            student_id = request.user.id
            student = main_models.User.objects.get(id=student_id)

            print("rate is ", rate)
            tutor = main_models.User.objects.get(id=tutor_id)

            rated = main_models.TutorRating.objects.create(
                rating="5",
                review=review,
                student=student,
                tutor=tutor
            )
            print("rating")
            rated.save()
            return tutor_profile(request,tutor_id)
        else:
            return redirect("tutor_login")
    else:
         return tutor_profile(request,tutor_id)
     
     
     
     
     
     
# payments

def payments(request):
    return render(request, 'saler/student/payments.html')

async def getAuthToken(request):
    url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"
    payload = json.dumps({
        "consumer_key": "INVBqKBsmVnVgdHiIYyqpJxSNIkNHp/K",
        "consumer_secret": "yRiA3QOS2pdzkoPfAAHAv3BOB+o="
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cookie': '__cf_bm=UkeRsH42trDKHeVZOlLjH_uLOmdQe8H_g3SBfPDyT44-1702363838-1-ATlP/7hc90zrXyGLz/go4//imcapHXvLOBhtK6LH1FEUsx3Ucx43KlmnAk/AE+uItRmmZFjktFP8VNmL5T91rB0='
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=payload)
        return response.json()


async def registerIpnUrl(request):
    try:
        data = await getAuthToken(request)
        token_value = data.get("token")
        url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"
        payload = json.dumps({
            "url": "http://127.0.0.1:8000/ipn",
            "ipn_notification_type": "GET"
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer  {token_value}',
            'Cookie': '__cf_bm=D6i0Q55cV0fAywZ6F2kYQPUc3BX0MVocklf0fNmAqhI-1702362813-1-AbM3loCbxQuLR18vRIpouqS9JX1CU/bZP17xcrk5+SQYgT1paOY3e3FDh3UFIb3mmKPaIXWlTMGbFmJWrZEMMdA='
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=payload)
            print(response.text)
        # return JsonResponse({'status': 'Data received successfully'})
        return response.text
    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({'status': 'Error fetching data'}, status=500)
    return HttpResponse("Hello World")

async def getTransactionStatus(request,order_tracking_id):
    # user = await sync_to_async(lambda:  request.user)()
    user= await sync_to_async(auth.get_user)(request)

    
    
    url = f"https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}"

    payload={}
    data = await getAuthToken(request)
    token_value = data.get("token")
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token_value}'
    }
    booking_payment = await sync_to_async(models.BookingPayments.objects.get)(order_tracking_id=order_tracking_id)
    
    
    
    async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            json_response = response.json()
            
    if json_response.get("payment_account"):
        booking_payment.payment_method=json_response.get("payment_method")
        booking_payment.create_date=json_response.get("create_date")
        booking_payment.confirmation_code=json_response.get("confirmation_code")
        booking_payment.payment_status_description=json_response.get("payment_status_description")
        booking_payment.message=json_response.get("message")
        booking_payment.currency=json_response.get("currency")
        booking_payment.payment_account=json_response.get("payment_account")
        booking_payment.status=json_response.get("status")
        booking_payment.create_date=json_response.get("created_date")
        booking_payment.payment_status_code=json_response.get("payment_status_code")
        await sync_to_async(booking_payment.save)()
        
        try:
            # existing_payment=await sync_to_async(models.MainFinanceAccount.objects.get)(last_deposit=booking_payment)
            existing_payment = await sync_to_async(models.MainFinanceAccount.objects.get)(last_deposit=booking_payment)

            # #uncomment for first time run
            # main_finance_account=await sync_to_async(models.MainFinanceAccount.objects.create)()
            # # latest_entry = await sync_to_async(models.MainFinanceAccount.objects.latest)()
            
            # main_finance_account.last_deposit=booking_payment
            # main_finance_account.last_deposit_amount=booking_payment.amount
            # main_finance_account.last_withdraw=0.00
            # main_finance_account.amount_balance=Decimal(str(0.0))+ main_finance_account.last_deposit_amount
            # saved_data = await sync_to_async(main_finance_account.save)()
            
            
            
            
        except models.MainFinanceAccount.DoesNotExist:
            latest_entry = await sync_to_async(models.MainFinanceAccount.objects.latest)()
            main_finance_account=await sync_to_async(models.MainFinanceAccount.objects.create)()
            main_finance_account.last_deposit=booking_payment
            main_finance_account.last_deposit_amount=booking_payment.amount
            main_finance_account.last_withdraw=0.00
            main_finance_account.amount_balance=Decimal(str(latest_entry.amount_balance)) + main_finance_account.last_deposit_amount
            saved_data = await sync_to_async(main_finance_account.save)()
            # saved_data.amount_balance = Decimal(str(main_finance_account.amount_balance)) + main_finance_account.last_deposit_amount
            # await sync_to_async(saved_data.save)()
            
            
            
        # save tutor finance account
        try:
            if await sync_to_async(lambda: booking_payment.booking)():
                tutor = await sync_to_async(lambda: booking_payment.booking.skill.tutor)()
                existing_tutor_account=await sync_to_async(models.TutorFinanceAccount.objects.get)(last_deposit__booking__skill__tutor=tutor)
                print("Payment for booking")
                
                
            else:
                tutor=await sync_to_async(lambda: booking_payment.course.tutor)()
                existing_tutor_account=await sync_to_async(models.TutorFinanceAccount.objects.get)(last_deposit__course__tutor=tutor)
                incoming_tutor_course =await sync_to_async(lambda: booking_payment.course.tutor)()
                existing_tutor = await sync_to_async(lambda: existing_tutor_account.last_deposit.course.tutor)()
                if incoming_tutor_course == existing_tutor:
                    print("This Iser alreday has existing account")
                    tutor_deposit = Decimal(booking_payment.amount) * Decimal('0.9')
                    existing_tutor_account.last_deposit_amount=Decimal(str(tutor_deposit))
                    existing_tutor_account.last_deposit=booking_payment
                    existing_tutor_account.last_withdraw=0.00
                    existing_tutor_account.amount_balance=Decimal(str(existing_tutor_account.amount_balance)) + existing_tutor_account.last_deposit_amount
                    await sync_to_async(existing_tutor_account.save)()
                else:
                    print("No previous payments")
                
           
            
            
            
            
            
            # if await sync_to_async(lambda: existing_tutor_account.last_deposit)() == await sync_to_async(lambda: booking_payment)():
            #     print("This is last deposit ")
            #     pass
            # else:
            #     print("this is a new deposit ")
            #     tutor_deposit = Decimal(booking_payment.amount) * Decimal('0.9')
            #     existing_tutor_account.last_deposit_amount=Decimal(str(tutor_deposit))
            #     existing_tutor_account.last_deposit=booking_payment
            #     existing_tutor_account.last_withdraw=0.00
            #     existing_tutor_account.amount_balance=Decimal(str(existing_tutor_account.amount_balance)) + existing_tutor_account.last_deposit_amount
            #     await sync_to_async(existing_tutor_account.save)()
            # #print("Tutor name is ",tutor.username)
        except models.TutorFinanceAccount.DoesNotExist:
            print("This is a a new Account")
            tutor_finance_account=await sync_to_async(models.TutorFinanceAccount.objects.create)()
            tutor_deposit = Decimal(booking_payment.amount) * Decimal('0.9')
            tutor_finance_account.last_deposit_amount=Decimal(str(tutor_deposit))
            tutor_finance_account.last_deposit=booking_payment
            tutor_finance_account.last_withdraw=0.00
            tutor_finance_account.amount_balance= Decimal(str(tutor_finance_account.amount_balance)) + tutor_finance_account.last_deposit_amount
            await sync_to_async(tutor_finance_account.save)()
            
        
        if await sync_to_async(lambda:  booking_payment.booking)():
            
            booking_id = await sync_to_async(lambda: booking_payment.booking.id)()
            booking = await sync_to_async(models.Booking.objects.get)(id=booking_id)
            booking.payment_status = models.Booking.PAYMENT_COMPLETED
            await sync_to_async(booking.save)()
        else:
            course_id=await sync_to_async(lambda: booking_payment.course.id)()
            course = await sync_to_async(models.Course.objects.get)(id=course_id)
            await sync_to_async(course.customers.add)(user)
            await sync_to_async(course.save)()
            
            print("Couse Data Saved ",course.customers)
        
        return redirect("studentTransactionHistory")
    else:
        booking_payment.status=json_response.get("status")
        await sync_to_async(booking_payment.save)()
        
        payment_id= await sync_to_async(lambda: booking_payment.booking.id)()
        booking = await sync_to_async(models.Booking.objects.get)(id=payment_id)
        booking.payment_status = models.Booking.PAYMENT_FAILED
        await sync_to_async(booking.save)()
        
        return redirect("studentTransactionHistory")
            # return response.text

async def submitOrder(request,booking_id,item,user_type):
 
    try:
        data = await getAuthToken(request)
        token_value = data.get("token")
        url = "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest"
        callback_url= await sync_to_async(reverse)("payments")
        named_url_absolute = request.build_absolute_uri(callback_url)


        
        
        # ipn id
        ipn_data=await registerIpnUrl(request)
        ipn_vals=json.loads(ipn_data)
        ipn_id_value = ipn_vals.get('ipn_id')
        
        uid = str(uuid.uuid4())
        current_datetime = str(datetime.now())
        
        if item == "booking":
            
            booking = await sync_to_async(models.Booking.objects.get)(id=booking_id)
            cost= str( await sync_to_async(lambda: booking.cost)())
        
        else:
           
            course = await sync_to_async(models.Course.objects.get)(id=booking_id)
            cost= str( await sync_to_async(lambda: course.cost)())
        
        user = await sync_to_async(lambda: request.user)()
        user_id =await sync_to_async(lambda: user.id)() 
        
        # user_details = await sync_to_async(main_models.UserDetail.objects.get)(user=user_id)
        email_address = await sync_to_async(lambda: user.email)()
        
        # student_details = await sync_to_async(main_models.StudentDetails.objects.filter)(user=request.user)
        # print("Details are",student_details)
        print("User is ",user_type)
        if user_type == "student":
            
            phone= await sync_to_async(lambda: request.user.studentdetails.contact_number)()
            
        else:
            phone= await sync_to_async(lambda: request.user.tutordetails.contact_number)()
        
        # phone= await sync_to_async(lambda: request.user.userdetails.mobile)()
        
        
        first_name= await sync_to_async(lambda: user.first_name)()
        last_name= await sync_to_async(lambda: user.last_name)()
        # cost= str( await sync_to_async(lambda: booking.cost)())
        
        print("1")
        
        

        payload = json.dumps({
            "id":uid ,
            "currency": "KES",
            "amount":"1" ,
            "description": "Payment For Tutor Session",
            "callback_url":named_url_absolute ,
            "redirect_mode": "",
            "notification_id": ipn_id_value,
            "branch": "LokoLingo",
            "billing_address": {
                "email_address": email_address,
                "phone_number": phone,
                "country_code": "KE",
                "first_name": first_name,
                "middle_name": "",
                "last_name": last_name,
                "line_1": "Pesapal Limited",
                "line_2": "",
                "city": "",
                "state": "",
                "postal_code": "",
                "zip_code": ""
            }
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token_value}',
            'Cookie': '__cf_bm=UkeRsH42trDKHeVZOlLjH_uLOmdQe8H_g3SBfPDyT44-1702363838-1-ATlP/7hc90zrXyGLz/go4//imcapHXvLOBhtK6LH1FEUsx3Ucx43KlmnAk/AE+uItRmmZFjktFP8VNmL5T91rB0='
        }
        
        user = request.user
        
        print("8455489")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=payload)
            
        print("2")

        json_response = response.json()
        redirect_url = json_response.get("redirect_url")
        
        
        tracking_id_value = json_response.get('order_tracking_id')
        print("3")
        booking_payment = await sync_to_async(models.BookingPayments.objects.create)()
        print("Reached Here")
        if tracking_id_value is not None:
            # if item is "booking":
            #     booking.student=request.user
          
            #     booking.payment_status = models.Booking.PAYMENT_INITIATED
            #     await sync_to_async(booking.save)()
            if item == "booking":
                print("vkjdf item is booking")
                booking_payment.booking=booking
            else:
                print("jvbdkjv item is course")
                booking_payment.course=course
                
            # booking_payment.booking=booking
            booking_payment.amount=1.00
            booking_payment.reference=json_response.get("merchant_reference")
            booking_payment.merchant_reference=json_response.get("merchant_reference")
            booking_payment.order_tracking_id=json_response.get("order_tracking_id")
            await sync_to_async(booking_payment.save)()
            
            
     
       
        
    
        
        if redirect_url:
            
            if user_type == "student":
          
                return render(request, 'saler/student/payments.html',{"redirect_url":redirect_url})
            
            else:
                return render(request, 'saler/admin/payments.html',{"redirect_url":redirect_url})
        else:
            # status = await getTransactionStatus(request,token_value,tracking_id_value)
            if user_type == "student":
                return render(request, 'saler/student/payments.html',{"tracking_id":tracking_id_value})
            else:
                
            
                return render(request, 'saler/admin/payments.html',{"tracking_id":tracking_id_value})
    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({'status': 'Error fetching data'}, status=500)

def checkTransactionHistory(request):
    user = request.user
   
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if 'student' in user_groups:
       
        transactions=models.BookingPayments.objects.filter(Q(booking__student=user) | Q(course__customers=user)).order_by("-id")
        # for item in  all_t:
        #     print("Course",item)
        
        context={
        "transactions":transactions
        }
        return render(request, "saler/student/payment_history.html",context)
    
    else:
        transactions=models.BookingPayments.objects.filter(Q(booking__skill__tutor=user) | Q(course__tutor=user)).order_by("-id")
        # transactions = models.BookingPayments.objects.filter(booking__skill__tutor=user).order_by("-id")
        context={
            "transactions":transactions
        }
        return render(request, "saler/admin/tutor_payment_history.html",context)
    
    
    
    
    # return render(request, "saler/student/payment_history.html",context)
    

def withdrawals(request):
    user=request.user
    saler_finances=models.TutorFinanceAccount.objects.filter(Q(last_deposit__booking__skill__tutor=user) | Q(last_deposit__course__tutor=user)).first()
    withdrawal_history = models.WithdrawFunds.objects.filter(Q(account__last_deposit__booking__skill__tutor=user) | Q(account__last_deposit__course__tutor=user)).order_by("-id")
    pending_withdrawal=0.00
    
    
    
    context = {
        "saler_finances":saler_finances,
        "withdraw_history":withdrawal_history
    }
    return render(request,"saler/admin/withdrawals.html",context)

def withdrawFundsForm(request):
    
    user = request.user
    account = models.TutorFinanceAccount.objects.filter(Q(last_deposit__booking__skill__tutor=user) | Q(last_deposit__course__tutor=user)).first()
    main_finance_account = models.MainFinanceAccount.objects.last()
    
    if request.method == "POST":
        try:
            pending_withdrawals = models.WithdrawFunds.objects.filter(Q(account__last_deposit__booking__skill__tutor=user) | Q(account__last_deposit__course__tutor=user)).last()
            messages.error(request,f'Please wait untill the pending withdraw request has been processed')
            if pending_withdrawals:
                if pending_withdrawals.status == "rejected" or pending_withdrawals.status == "processed" or pending_withdrawals.status == "cancelled":
                    amount = request.POST.get("amount")
                    
                    withdraw_request = models.WithdrawFunds.objects.create(
                        amount=amount,
                        account=account
                    )
                    
                    account.amount_balance = account.amount_balance-Decimal(str(amount))
                    account.save()
                    withdraw_request.save()
                    
                    update_finance = models.MainFinanceAccount.objects.create(
                        transaction_type = models.MainFinanceAccount.WITHDRAW,
                        amount_balance = main_finance_account.amount_balance - Decimal(str(amount)),
                        last_withdraw = Decimal(str(amount)),
                        last_deposit_amount=main_finance_account.last_deposit_amount
                        
                        
                    )
                    
                    update_finance.save()
                    
                    return redirect("withdrawals")
            else:
                amount = request.POST.get("amount")
                    
                withdraw_request = models.WithdrawFunds.objects.create(
                    amount=amount,
                    account=account
                )
                withdraw_request.save()
                
                update_finance = models.MainFinanceAccount.objects.create(
                        transaction_type = models.MainFinanceAccount.WITHDRAW,
                        amount_balance = main_finance_account.amount_balance - Decimal(str(amount)),
                        last_withdraw = Decimal(str(amount)),
                        last_deposit_amount=main_finance_account.last_deposit_amount
                        
                        
                    )
                    
                update_finance.save()
                account.amount_balance = account.amount_balance-Decimal(amount)
                account.save()
                return redirect("withdrawals")
            return redirect("withdrawals")
        except models.WithdrawFunds.DoesNotExist:
                
            amount = request.POST.get("amount")
            
            withdraw_request = models.WithdrawFunds.objects.create(
                amount=amount,
                account=account
            )
            update_finance = models.MainFinanceAccount.objects.create(
                        transaction_type = models.MainFinanceAccount.WITHDRAW,
                        amount_balance = main_finance_account.amount_balance - Decimal(str(amount)),
                        last_withdraw = Decimal(str(amount)),
                        last_deposit_amount=main_finance_account.last_deposit_amount
                        
                        
                    )
                    
            update_finance.save()
            withdraw_request.save()
            account.amount_balance = account.amount_balance-Decimal(amount)
            account.save()
            return redirect("withdrawals")
    
    else:
        return redirect("saler_account_settings")

def cancelWithdrawRequest(request,withdraw_id):
    withdraw_request = models.WithdrawFunds.objects.get(id=withdraw_id)
    user = request.user
    account = models.TutorFinanceAccount.objects.filter(Q(last_deposit__booking__skill__tutor=user) | Q(last_deposit__course__tutor=user)).first()
    main_finance_account = models.MainFinanceAccount.objects.last()
    
    withdraw_request.status=withdraw_request.CANCELLED
    account.amount_balance = account.amount_balance + withdraw_request.amount
    
    
    withdraw_request.save()
    account.save()
    
    update_finance = models.MainFinanceAccount.objects.create(
                        transaction_type = models.MainFinanceAccount.WITHDRAW,
                        amount_balance = main_finance_account.amount_balance + Decimal(str(withdraw_request.amount)),
                        last_withdraw = Decimal(str(withdraw_request.amount)),
                        last_deposit_amount=main_finance_account.last_deposit_amount
                        
                        
                    )
                    
    update_finance.save()
    
    return redirect("withdrawals")
    
def courseManagement(request):
    request.session['redirect_to'] = request.build_absolute_uri()
    user = request.user
    courses = models.Course.objects.filter(tutor=user)
    context={
        "courses":courses
    }
    
    return render(request,"saler/admin/courses.html",context)

def addCourse(request):
    course_form = forms.AddCourseForm(request.POST,request.FILES)
    context = {
    "form":course_form
    }
    
    if request.method == "POST":
        
        if course_form.is_valid():
                form = course_form.save(commit=False)
                form.tutor=request.user
                form.save()
                messages.success(request,"Course Added")
                return redirect("courseManagement")

   
    
    return render(request,"saler/admin/add_course.html",context)  

def courseDetails(request,course_id):
    course=models.Course.objects.get(id=course_id)
    context={
        "course":course
    }
    
    return render(request,"saler/admin/course_details.html",context) 



def adminCourseResources(request,course_id):
    course=models.Course.objects.get(id=course_id)
    sections=models.CourseSection.objects.filter(course=course)
    
    
    
    section_form=forms.AddCourseSectionForm()
    section_resource_form=forms.AddSectionResurceForm()
    
    if request.method == "POST":
        section_form=forms.AddCourseSectionForm(request.POST)
        if section_form.is_valid():
            form=section_form.save(commit=False)
            form.course=course
            form.save()
            print("Saved")
            
        else:
            print("Invalid form")
    
    
    context={
        "sections":sections,
        "section_form":section_form,
        "section_resource_form":section_resource_form
    }
    
    user = request.user
   
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if 'student' in user_groups:
        return render(request,"saler/student/student_course_resources.html",context)
    else:
        
    
        return render(request,"saler/admin/course_resources.html",context)

def addSectionResource(request,section_id,course_id):
    # course_id = request.GET.
    section = models.CourseSection.objects.get(id=section_id)
    form = forms.AddSectionResurceForm(request.POST,request.FILES)
    if form.is_valid():
        section_form = form.save(commit=False)
        section_form.section=section
        section_form.save()
        print("resource saved")
        return redirect("adminCourseResources",course_id=course_id)  
    else:
        print('Not saved')

        return redirect("adminCourseResources",course_id=course_id)


def editSection(request,section_id):
    
    
    return redirect


def deleteSection(request,section_id,course_id):
    # course_id = request.GET.get("course_id")
    
    section = models.CourseSection.objects.get(id=section_id)
    section.delete()
    
    
    return redirect("adminCourseResources",course_id=course_id)
    

def editResource(request,resource_id,course_id):
    resource = models.SectionVideo.objects.get(id=resource_id)
    if request.method == "GET":
        form = forms.AddSectionResurceForm(instance=resource)
        
    return redirect("adminCourseResources",course_id=course_id)



def deleteResource(request,resource_id,course_id):
    resource=models.SectionVideo.objects.get(id=resource_id)
    resource.delete()
    return redirect("adminCourseResources",course_id=course_id)


def tutorSessions(request):
    user=request.user
    form = forms.UpdateSessionForm()
    
   
        
    
    sessions = models.TutorSession.objects.filter(payments__booking__skill__tutor=user)
    context={
        "sessions":sessions,
        "form":form
    }
    
    if request.method == "POST":
        form = forms.UpdateSessionForm(request.POST)
        
        form.save()
        print("Form Saved")
        return render(request,"saler/admin/sessions.html",context)
    else:
        return render(request,"saler/admin/sessions.html",context)


def updateSessionStatus(request,session_id):
    session = models.TutorSession.objects.get(id=session_id)
    user=request.user
    form = forms.UpdateSessionForm()
    sessions = models.TutorSession.objects.filter(payments__booking__skill__tutor=user)
    context={
        "sessions":sessions,
        "form":form
    }
    if request.method == "POST":
        form = forms.UpdateSessionForm(request.POST,instance=session)
        
        form.save()
        print("Form Saved")
        return render(request,"saler/admin/sessions.html",context)
    else:
        return render(request,"saler/admin/sessions.html",context)
    
    


def createSession(request,booking_id):
    booking=models.Booking.objects.get(id=booking_id)
    payments=models.BookingPayments.objects.get(booking=booking)
    
  
    decimal_hours = Decimal(booking.duration)
    total_seconds = float(decimal_hours) * 3600
    duration_timedelta = timedelta(seconds=total_seconds)
    
    hours, remainder = divmod(duration_timedelta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    time =''

    if hours > 0:
        time =  f"{hours} hours and {minutes} minutes"
    else:
        time = f"{minutes} minutes"
    
    booking.duration=time
    # used_payment=models.TutorSession.objects.get(payments__reference=payments.reference)
    
    context={
        "booking":booking,
        "payments":payments
        }
    
    try:
        # used_payment=models.TutorSession.objects.get(payments__reference=payments.reference)
        messages.error(request, f'A session using this payment has already been created')
        used_payment=get_object_or_404(models.TutorSession,payments__reference=payments.reference)
        return render(request,"saler/admin/create_session.html",context)
    except Exception as e:
    
        if request.method == "POST":
            title=request.POST.get("title")
            meet_url=request.POST.get("meet")
            
           
            session = models.TutorSession.objects.create()
            session.title=title
            session.meet_url=meet_url
            session.session_status=models.TutorSession.NOT_STARTED
            session.payments=payments
            session.save()
            # messages.error(request, f'Invalid username or password')
            messages.success(request, f'Session Created Succesfully')
            return redirect("tutorSessions")
    
    
    return render(request,"saler/admin/create_session.html",context)

def withdrawFunds(request):
    pass


# This is a part of admin view in which all ordered products will display with address
def admin2(request):
    if request.user.is_superuser:
        ordr = [i for i in Orders.objects.all() if i.status != 'Cancel' and i.status !=
                'On The Way' and i.status != 'Delivered'][::-1]
        params = {
            'orders': ordr,
            'dorders': [i for i in Orders.objects.filter(saler=request.user) if i.status != 'Cancel' and i.status == 'On The Way' or i.status == 'Delivered'],
            'cart_element_no': len([p for p in MyCart.objects.all() if p.user == request.user]),
        }
        return render(request, 'saler/admin2.html', params)
    else:
        return redirect("/")



def chatView(request):
    
    
    return render(request,'saler/frontpage.html')

def studentChat(request,tutor_id):
    # tutor = models.UserDetail.objects.get(id=skill_id)
    tutor = main_models.UserDetail.objects.get(user = tutor_id)
    try:
        
        room_name = str(tutor.user.username) + "-" + str(request.user.username)+"-Room"
    
        student_room = room_models.Room.objects.create(
            name = room_name,
            slug=room_name,
            student=request.user,
            tutor=tutor.user
        )
        messages = room_models.Message.objects.filter(room=student_room)[0:25]
        
        context={
            "room":student_room,
            "messages":messages
        }
        
        return render(request,"saler/student/chat_screen.html",context)
        # return render(request, 'room/room.html', {'room':student_room,"messages":messages})
    
    except Exception as e:
        print("Error creting room ",e)
        room = room_models.Room.objects.get(student=request.user,tutor=tutor.user)
        messages = room_models.Message.objects.filter(room=room)[0:25]
        context={
            "room":room,
            "messages":messages
        }
        return render(request,"saler/student/chat_screen.html",context)
        # return render(request,"saler/student/student_home.html")
    
def chatRoom(request,room_id):
    room = room_models.Room.objects.get(id=room_id)
    messages = room_models.Message.objects.filter(room=room)[0:25]
        
    context={
        "room":room,
        "messages":messages
    }
        
    return render(request,"saler/student/chat_screen.html",context)

def staffChatRoom(request,room_id):
    print("room id is ",room_id)
    room = room_models.Room.objects.get(id=room_id)
    messages = room_models.Message.objects.filter(room=room)[0:25]
        
    context={
        "room":room,
        "messages":messages
    }
        
    return render(request,"saler/admin/staff_chat.html",context)