from datetime import datetime
from decimal import Decimal
import json
import math
import uuid
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
from . import models
from asgiref.sync import sync_to_async
from django.db.models import Count


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




def tutor_signup(request):
    if request.user.is_authenticated:
        user=request.user
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'student' in user_groups:
            return redirect("studentDashboard")
        
        else:
            
            return redirect('saler_account_settings')
        
        # return redirect('saler_account_settings')
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
            
            
            # if user_type in dict()
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(
                    request, 'User with this username or email already exists.')
                return render(request, 'saler/tutor_signup.html')  # Redirect back to the signup page

            hashed_password = make_password(password)
            user = User.objects.create(
                username=username, email=email, password=hashed_password, first_name=firstname, last_name=lastname, )
            
            user.save()
            group_name = 'student' if user_type == 'student' else 'tutor'
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
            
            messages.success(request, 'Account created successfully!')
            # print(user.groups.name)
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
            return redirect('tutor_login')

            
    return render(request, 'saler/tutor_signup.html')


def tutor_login(request,next_page=None):
    username = request.POST.get('username')
    password = request.POST.get('password')
    ab = request.build_absolute_uri(reverse("home"))
    print("next page us ",ab)
    referring_url = request.META.get('HTTP_REFERER', None)
    request.session["previous_page"] = referring_url
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        messages.success(request, f'Hi {username.title()}, welcome back!')
        user_groups = request.user.groups.values_list('name', flat=True)
        if next_page == ab:
            print("Next paaage is ",next_page)
            if 'student' in user_groups:
                return redirect("studentDashboard")
            else:
                return redirect('saler_account_settings')
        else:
            print("Next paaadfdge is ",next_page)
            return redirect(next_page)
    messages.error(request, f'Invalid username or password')
    print("Not Authenticated")
    url = reverse('tutor_signup') + f'?next_page={reverse("home") if referring_url is None else referring_url}'
    return redirect(url)






# Seller Account Settings


@login_required
def account_settings(request):
    user=request.user
    saler_finances=models.TutorFinanceAccount.objects.filter(last_deposit__booking__skill__tutor=user).first()
    withdrawal_history = models.WithdrawFunds.objects.filter(account__last_deposit__booking__skill__tutor=user)
    skills = models.Skill.objects.filter(tutor=user)
    rooms = room_models.Room.objects.filter(tutor = request.user).annotate(message_count=Count('messages'))
    transactions = models.BookingPayments.objects.filter(booking__skill__tutor=user).order_by("-id")
    
    context={
        "saler_finances":saler_finances,
        "skills":skills,
        "withdrawals":withdrawal_history,
        "rooms":rooms,
        "transactions":transactions
    }
    return render(request, 'saler/admin/home.html',context)

def studentDashboard(request):
    user=request.user
    sessions = models.TutorSession.objects.filter(payments__booking__student=user)
    rooms = room_models.Room.objects.filter(student=user).annotate(message_count=Count('messages'))
    print("Student rooms count", rooms.count())
    context={
        "sessions":sessions,
        "rooms":rooms
    }
    return render(request,"saler/student/student_home.html",context)


def studentBookings(request):
    student_id=request.user.id
    bookings = models.Booking.objects.filter(student=student_id)
    context={
        "bookings":bookings
    }
    return render(request,"saler/student/student_bookings.html",context)


def studentProfile(request):
    form = UpdateStudentProfileForm()
    try:
        # user_details = main_models.UserDetail.objects.filter(user_id=request.user.id)
        print(request.user.id)
        user_details= get_object_or_404(main_models.UserDetail,user=request.user.id)
        print(request.user.id)
        return render(request, "saler/student/student_profile.html", {'user_details': user_details})
    except Http404:
        return updateStudentProfile(request)

def updateStudentProfile(request):
    form = UpdateStudentProfileForm()
    print(request.method)
    if request.method == "POST":
       
        form = UpdateStudentProfileForm(request.POST,request.FILES)
        if form.is_valid():
            tutor = form.save(commit=False)
            tutor.user_type = "student"
            tutor.save()
            messages.success(request,"Profile Updated")
            print("form saved")
            return redirect("studentDashboard")
        else:
            print("invalid form")
            return render(request,"saler/student/student_profile.html",{'profile_form':form})
    else:
       
        return render(request,"saler/student/student_profile.html",{'profile_form':form})


def updateProfile(request):
    form = UpdateUserDetailForm()
    try:
        # user_details = main_models.UserDetail.objects.filter(user_id=request.user.id)
        print(request.user.id)
        user_details= get_object_or_404(main_models.UserDetail,user=request.user.id)
        print(request.user.id)
        return render(request, "saler/admin/profile.html", {'user_details': user_details})
    except Http404:
        return updateProfileForm(request)

    

def updateProfileForm(request):
    form = UpdateUserDetailForm()
    print(request.method)
    if request.method == "POST":
       
        form = UpdateUserDetailForm(request.POST,request.FILES)
        if form.is_valid():
            tutor = form.save(commit=False)
            tutor.user_type = "tutor"
            tutor.save()
            messages.success(request,"Profile Updated")
            print("form saved")
            return redirect("saler_account_settings")
        else:
            print("invalid form")
            return render(request,"saler/admin/profile.html",{'profile_form':form})
    else:
       
        return render(request,"saler/admin/profile.html",{'profile_form':form})
          
@login_required
def addSkill(request):
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
    
    booking_form=forms.BookingStatusUpdateForm(request.POST)
    context = {
        "bookings":bookings,
        "form":booking_form
    }

    return render(request,"saler/admin/bookings.html",context)

def update_booking_status(request, booking_id):
    booking = get_object_or_404(models.Booking, id=booking_id)
    tutor_id = request.user.id
    bookings = models.Booking.objects.filter(skill__tutor=tutor_id)
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
    # print(tutor_id)
    tutor = main_models.UserDetail.objects.get(user = tutor_id)
    skills = models.Skill.objects.filter(tutor=tutor_id)
    tutor_rating = main_models.TutorRating.objects.filter(tutor=tutor.user)
    
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
        "tutor_reviews":tutor_rating
    }
    return render(request,"saler/tutor_profile.html",context)

# @login_required
def bookSession(request,tutor_id):
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        message= request.POST.get("message")
        skill_id = request.POST.get("skill")
        duration = request.POST.get("duration")
        skill = models.Skill.objects.get(id=skill_id)
        # tutor=models.User.objects.get(id=tutor_id)
        
        if request.user.is_authenticated:
            user = request.user
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
        else:
            return redirect("tutor_login")
        
        
        return redirect("studentBookings")
    else:
        return redirect("studentBookings")
    

def rateTutor(request,tutor_id):
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
            existing_payment=await sync_to_async(models.MainFinanceAccount.objects.get)(last_deposit=booking_payment)
            # uncomment for first time run
            # main_finance_account=await sync_to_async(models.MainFinanceAccount.objects.create)()
            # latest_entry = await sync_to_async(models.MainFinanceAccount.objects.latest)()
            
            # main_finance_account.last_deposit=booking_payment
            # main_finance_account.last_deposit_amount=booking_payment.amount
            # main_finance_account.last_withdraw=0.00
            # main_finance_account.amount_balance=Decimal(str(latest_entry.amount_balance)) + main_finance_account.last_deposit_amount
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
            tutor = await sync_to_async(lambda: booking_payment.booking.skill.tutor)()
            existing_tutor_account=await sync_to_async(models.TutorFinanceAccount.objects.get)(last_deposit__booking__skill__tutor=tutor)
            tutor_deposit = Decimal(booking_payment.amount) * Decimal('0.7')
            existing_tutor_account.last_deposit_amount=Decimal(str(tutor_deposit))
            existing_tutor_account.last_deposit=booking_payment
            existing_tutor_account.last_withdraw=0.00
            existing_tutor_account.amount_balance=Decimal(str(existing_tutor_account.amount_balance)) + existing_tutor_account.last_deposit_amount
            await sync_to_async(existing_tutor_account.save)()
            # print("Tutor name is ",tutor.username)
        except models.TutorFinanceAccount.DoesNotExist:
            tutor_finance_account=await sync_to_async(models.TutorFinanceAccount.objects.create)()
            tutor_deposit = Decimal(booking_payment.amount) * Decimal('0.7')
            tutor_finance_account.last_deposit_amount=Decimal(str(tutor_deposit))
            tutor_finance_account.last_deposit=booking_payment
            tutor_finance_account.last_withdraw=0.00
            tutor_finance_account.amount_balance= Decimal(str(tutor_finance_account.amount_balance)) + tutor_finance_account.last_deposit_amount
            await sync_to_async(tutor_finance_account.save)()
            
        
        booking_id = await sync_to_async(lambda: booking_payment.booking.id)()
        booking = await sync_to_async(models.Booking.objects.get)(id=booking_id)
        booking.payment_status = models.Booking.PAYMENT_COMPLETED
        await sync_to_async(booking.save)()
       
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

async def submitOrder(request,booking_id):
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
        
        booking = await sync_to_async(models.Booking.objects.get)(id=booking_id)
        # rate_per_hour = await sync_to_async(lambda: booking.skill.tutor.userdetails.rate_per_hour)()
        # duration = await sync_to_async(lambda: booking.duration)()
        
        # cost =str(Decimal(rate_per_hour)*Decimal(duration))

        
        user = await sync_to_async(lambda: request.user)()
        user_id =await sync_to_async(lambda: user.id)() 
      
        user_details = await sync_to_async(main_models.UserDetail.objects.get)(user=user_id)
        email_address = await sync_to_async(lambda: user.email)()
        phone= await sync_to_async(lambda: request.user.userdetails.mobile)()
        first_name= await sync_to_async(lambda: user.first_name)()
        last_name= await sync_to_async(lambda: user.last_name)()
        cost= str( await sync_to_async(lambda: booking.cost)())
        
        
        
        

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
        
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=payload)
            

        json_response = response.json()
        redirect_url = json_response.get("redirect_url")
        
        
        tracking_id_value = json_response.get('order_tracking_id')
        
        booking_payment = await sync_to_async(models.BookingPayments.objects.create)()
        print("Reached Here",booking_id)
        if tracking_id_value is not None:
            booking.student=request.user
          
            booking.payment_status = models.Booking.PAYMENT_INITIATED
            await sync_to_async(booking.save)()
            
            booking_payment.booking=booking
            booking_payment.amount=1.00
            booking_payment.reference=json_response.get("merchant_reference")
            booking_payment.merchant_reference=json_response.get("merchant_reference")
            booking_payment.order_tracking_id=json_response.get("order_tracking_id")
            await sync_to_async(booking_payment.save)()
            
            
     
       
        
    
        
        if redirect_url:
          
            return render(request, 'saler/student/payments.html',{"redirect_url":redirect_url})
        else:
            # status = await getTransactionStatus(request,token_value,tracking_id_value)
            
            return render(request, 'saler/student/payments.html',{"tracking_id":tracking_id_value})
    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({'status': 'Error fetching data'}, status=500)

def checkTransactionHistory(request):
    user = request.user
   
    user_groups = request.user.groups.values_list('name', flat=True)
    
    if 'student' in user_groups:
        transactions = models.BookingPayments.objects.filter(booking__student=user).order_by("-id")
        context={
        "transactions":transactions
        }
        return render(request, "saler/student/payment_history.html",context)
    
    else:
        transactions = models.BookingPayments.objects.filter(booking__skill__tutor=user).order_by("-id")
        context={
            "transactions":transactions
        }
        return render(request, "saler/admin/tutor_payment_history.html",context)
    
    
    
    
    # return render(request, "saler/student/payment_history.html",context)
    

def withdrawals(request):
    user=request.user
    saler_finances=models.TutorFinanceAccount.objects.filter(last_deposit__booking__skill__tutor=user).first()
    withdrawal_history = models.WithdrawFunds.objects.filter(account__last_deposit__booking__skill__tutor=user).order_by("-id")
    pending_withdrawal=0.00
    
    
    
    context = {
        "saler_finances":saler_finances,
        "withdraw_history":withdrawal_history
    }
    return render(request,"saler/admin/withdrawals.html",context)

def withdrawFundsForm(request):
    
    user = request.user
    account = models.TutorFinanceAccount.objects.get(last_deposit__booking__skill__tutor=user)
    main_finance_account = models.MainFinanceAccount.objects.last()
    
    if request.method == "POST":
        try:
            pending_withdrawals = models.WithdrawFunds.objects.filter(account__last_deposit__booking__skill__tutor=user).last()
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
    account = models.TutorFinanceAccount.objects.get(last_deposit__booking__skill__tutor=user)
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

 

def tutorSessions(request):
    user=request.user
    sessions = models.TutorSession.objects.filter(payments__booking__skill__tutor=user)
    context={
        "sessions":sessions
    }
    return render(request,"saler/admin/sessions.html",context)

def createSession(request,booking_id):
    booking=models.Booking.objects.get(id=booking_id)
    payments=models.BookingPayments.objects.get(booking=booking)
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