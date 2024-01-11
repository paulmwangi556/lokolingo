from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

class SalerDetail(models.Model):
	SEX_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
	STATE_CHOICES = (
		("Githurai",'Githurai'),
		("Kahawa",'Kahawa'),
		("Ruiru",'Ruiru'),
		("Juja",'Juja'),
		("Kasarani",'Kasarani'),
		("Thika",'Thika'),
		("Kayole",'Kayole'),
		("Eastleigh",'Eastleigh'),
		("CBD",'CBD'),
		("Westlands",'Westlands'),
		("Kibera",'Kibera'),
		("Kayole",'Kayole'),
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,)
	photo = models.ImageField(default='default.png',upload_to='user_photos')
	mobile = models.CharField(max_length=10,null=True)
	gst_Number = models.CharField(max_length=15,null=True)
	# shop_Name = models.CharField(max_length=500,null=True)
	alternate_mobile = models.CharField(max_length=10,null=True,blank=True)
	shop_Address = models.TextField()
	pincode = models.CharField(max_length=6, null=True)
	landmark = models.CharField(max_length=500, null=True, blank=True)
	locality = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	area = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
	account_Holder_Name = models.CharField(max_length=50, null=True)
	account_Number = models.CharField(max_length=20, null=True)
	ifsc_Code = models.CharField(max_length=11, null=True)

	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)

	# 	img = Image.open(self.photo.path)
	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.photo.path)
 
class SkillCategory(models.Model):
    category = models.CharField(max_length=100,default="General") 
    
    def __str__(self) -> str:
	               return self.category
	

class Skill(models.Model):
    title = models.CharField(max_length=100)
    tutor= models.ForeignKey(User,on_delete=models.DO_NOTHING)
    category = models.ForeignKey(SkillCategory,on_delete=models.DO_NOTHING)
   
    description= models.TextField()
    thumbnail = models.FileField(upload_to="skill_images",default='default.png')
    
    
    
class TimeSlots(models.Model):
    skill = models.ForeignKey(Skill,on_delete=models.DO_NOTHING,related_name="slots")
    start_time=models.TimeField()
    end_time=models.TimeField()
    is_booked=models.BooleanField(default=False)
    date=models.DateField()


class Booking(models.Model):
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    PENDING_PAYMENT = 'pending_payment'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ARCHIVED = 'archived'
    ON_HOLD = 'on_hold'

    STATUS_CHOICES = [
		(PENDING_APPROVAL, 'Pending Approval'),
		(APPROVED, 'Approved'),
		(REJECTED, 'Rejected'),
		(CANCELLED, 'Cancelled'),
		(PENDING_PAYMENT, 'Pending Payment'),
		(CONFIRMED, 'Confirmed'),
		(IN_PROGRESS, 'In Progress'),
		(COMPLETED, 'Completed'),
		
	]

    PAYMENT_NOT_INITIATED='payment_not_initiated'
    PAYMENT_INITIATED='payment_initiated'
    PAYMENT_PENDING = 'payment_pending'
    PAYMENT_COMPLETED = 'payment_completed'
    PAYMENT_FAILED = 'payment_failed'
	

    PAYMENT_STATUS_CHOICES = [
		(PAYMENT_NOT_INITIATED,'Payment Not Initiated'),
		(PAYMENT_INITIATED,'Payment Initiated'),
        (PAYMENT_PENDING, 'Payment Pending'),
        (PAYMENT_COMPLETED, 'Payment Completed'),
        (PAYMENT_FAILED, 'Payment Failed'),
    ]

    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING_APPROVAL,
    )
    # tutor = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True,related_name="tutor_details")
    skill = models.ForeignKey(Skill,on_delete=models.DO_NOTHING,blank=True,null=True)
    student=models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True,related_name="student_details")
    date=models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True,null=True)
    student_message = models.TextField(blank=True,null=True)
    tutor_message = models.TextField(blank=True,null=True)
    duration = models.CharField(max_length=5,default="1")
    cost=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    payment_status = models.CharField(
        max_length=30,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_NOT_INITIATED,
    )
    
def booking_post_save(sender,instance,created,*args,**kwargs):
    instance.cost = Decimal(instance.skill.tutor.tutordetails.hourly_rate) * Decimal(instance.duration) 
    if created:
        instance.save()
        
        
post_save.connect(booking_post_save,sender=Booking)

    
class InitiatedPayments():
    tracking_id=models.CharField(max_length=100)
 
class Course(models.Model):
    name=models.CharField(verbose_name="Course Name",max_length=100,blank=True,null=True)
    description=models.TextField(blank=True,null=True,verbose_name="Course Description")
    thumbnail=models.FileField(upload_to="course_images",blank=True,null=True)
    cost = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    language = models.CharField(max_length=100,blank=True,null=True)
    subtitles=models.TextField(null=True,blank=True,verbose_name="Other Languages or Subtitles")
    tutor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="course_tutor")
    course_content=models.TextField(blank=True,null=True)
    preview = models.FileField(upload_to="course_previews",blank=True,null=True,verbose_name="Course Preview Video")
    prerequisite=models.TextField(blank=True,null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    customers = models.ManyToManyField(User,blank=True,null=True)
    course_files = models.FileField(upload_to="course_files",blank=True,null=True)
    other_information=models.TextField(blank=True,null=True,verbose_name="Additional Information about the Course")
    date_added = models.DateField(auto_now_add=True)

class CourseSection(models.Model):
    index=models.IntegerField(verbose_name="Index (used in ordering)", blank=True,null=True)
    title=models.CharField(max_length=100,verbose_name="Section Title")
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    
    class Meta:
        ordering=["index"]
    

    
class SectionVideo(models.Model):
	index=models.IntegerField(verbose_name="Index (used in ordering)", blank=True,null=True)
	title=models.CharField(max_length=100,verbose_name="Video Title")
	resource_file=models.FileField(upload_to="section_videos")
	section=models.ForeignKey(CourseSection,on_delete=models.CASCADE)
 
	class Meta:
		ordering = ['index']

class CourseRating(models.Model):
    
    RATE=[
		("1","1"),
		("2","2"),
		("3","3"),
		("4","4"),
		("5","5")
	]
    
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True)
    rating = models.CharField(max_length=10,choices=RATE)
    review = models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)	
    
class BookingPayments(models.Model):
	booking = models.ForeignKey(Booking,on_delete=models.DO_NOTHING,null=True,blank=True)
	course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True,blank=True)
	amount = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	date=models.DateTimeField(auto_now_add=True)
	reference = models.CharField(max_length=10,null=True,blank=True)
	payment_method=models.CharField(max_length=100,null=True,blank=True)
	confirmation_code = models.CharField(max_length=100,null=True,blank=True)
	payment_status_description=models.CharField(max_length=100,null=True,blank=True)
	payment_account = models.CharField(max_length=50,null=True,blank=True)
	merchant_reference=models.CharField(max_length=100,null=True,blank=True)
	currency=models.CharField(max_length=100,null=True,blank=True)
	order_tracking_id=models.CharField(max_length=100,null=True,blank=True)
	create_date=models.DateTimeField(null=True,blank=True)
	message=models.CharField(max_length=100,blank=True,null=True)
	status_code=models.CharField(max_length=20,blank=True,null=True)
	payment_status_code = models.CharField(max_length=20,null=True,blank=True)
	status = models.CharField(max_length=20,null=True,blank=True)
 
	
	
	


# class TutorAccount(models.Model):
#     balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
#     tutor = models.ForeignKey(User,on_delete=models.DO_NOTHING)
#     last_deposit_amount = models.ForeignKey(BookingPayments,on_delete=models.DO_NOTHING)

class SellerSlider(models.Model):
	name = models.CharField(max_length=50, default = "", null=True)
	image = models.ImageField(upload_to='seller_slider_img')
	url = models.CharField(max_length=200, default = "#", null=True)

	def __str__(self):
		return f'{self.name}'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)
		if img.height > 1024 or img.width > 1024:
			output_size = (1024, 1024)
			img.thumbnail(output_size)
			img.save(self.image.path)


class category(models.Model):
	name = models.CharField(max_length=50, default="")
	sub_Categories  = models.TextField(default="")
	def __str__(self):
		return f'{self.name}'


class TutorSession(models.Model):
	NOT_STARTED = 'not_started'
	ONGOING = 'ongoing'
	COMPLETED = 'completed'
	
	CANCELLED = 'cancelled'
	

	SESSION_STATUS_CHOICES = [
		(NOT_STARTED, 'Not Started'),
		(ONGOING, 'Ongoing'),
		(COMPLETED, 'Completed'),
		
		(CANCELLED, 'Cancelled'),
		
	]

	session_status = models.CharField(
		max_length=20,
		choices=SESSION_STATUS_CHOICES,
		default=NOT_STARTED,
	)
	title =models.CharField(max_length=200,blank=True,null=True)
	payments = models.ForeignKey(BookingPayments,on_delete=models.DO_NOTHING,blank=True,null=True,related_name="session")
	meet_url = models.CharField(max_length=200,blank=True,null=True)
	
 
class MainFinanceAccount(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    
    STATUS_CHOICES = [
		(DEPOSIT,'Deposit'),
		(WITHDRAW,'Withdraw')
	]
    
    transaction_type = models.CharField(max_length=20,choices=STATUS_CHOICES,default=DEPOSIT)
    amount_balance=models.DecimalField(default=0.00,decimal_places=2,max_digits=5,blank=True,null=True)
    last_withdraw=models.DecimalField(decimal_places=2,max_digits=10,blank=True,null=True)
    last_deposit_amount=models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    last_deposit=models.ForeignKey(BookingPayments,on_delete=models.DO_NOTHING,blank=True,null=True)   
    
    
    class Meta:
        get_latest_by = 'id'
class TutorFinanceAccount(models.Model):
    amount_balance=models.DecimalField(default=0.00,decimal_places=2,max_digits=10,blank=True,null=True)
    last_withdraw=models.DecimalField(decimal_places=2,max_digits=10,blank=True,null=True)
    last_deposit_amount=models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    last_deposit=models.ForeignKey(BookingPayments,on_delete=models.DO_NOTHING,blank=True,null=True)

class WithdrawFunds(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PROCESSED = 'processed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELLED,'Cancelled'),
        (PROCESSED, 'Processed'),
    ]
    
    date_initiated = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    account = models.ForeignKey(TutorFinanceAccount,on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)


    


    
class Product(models.Model):
	GST_CHOICES = (("0",'0'),("3",'3'),("5",'5'),("12",'12'),("18",'18'),("28",'28'))
	product_id = models.BigAutoField(primary_key=True)
	product_id2 = models.CharField(max_length=100,default='')
	shop = models.ForeignKey(User, on_delete=models.CASCADE,default='')
	product_name = models.CharField(max_length=100, default="")
	prod_seller = models.CharField(max_length=100, default="")
	category = models.ForeignKey(category, default="", verbose_name="Category", on_delete=models.SET_DEFAULT, null=True)
	subcategory = models.CharField(max_length=50, default="")
	price = models.IntegerField(default=0)
	# price_not = models.IntegerField(default=999)
	desc = models.TextField()
	gst = models.CharField(default='0',max_length=3,choices=GST_CHOICES)
	pub_date = models.DateField(auto_now=True)
	image1 = models.ImageField(upload_to='products/images', default="",null=True)
	image2 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image3 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image4 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image5 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img1 = Image.open(self.image1.path)
		if img1.height > 1500 or img1.width > 1500:
			output_size = (1500, 1500)
			img1.thumbnail(output_size)
			img1.save(self.image1.path)
		if self.image2:
			img2 = Image.open(self.image2.path)
			if img2.height > 1500 or img2.width > 1500:
				output_size = (1500, 1500)
				img2.thumbnail(output_size)
				img2.save(self.image2.path)

		if self.image3:
			img3 = Image.open(self.image3.path)
			if img3.height > 1500 or img3.width > 1500:
				output_size = (1500, 1500)
				img3.thumbnail(output_size)
				img3.save(self.image3.path)

		if self.image4:
			img4 = Image.open(self.image4.path)
			if img4.height > 1500 or img4.width > 1500:
				output_size = (1500, 1500)
				img4.thumbnail(output_size)
				img4.save(self.image4.path)

		if self.image5:
			img5 = Image.open(self.image5.path)
			if img5.height > 1500 or img5.width > 1500:
				output_size = (1500, 1500)
				img5.thumbnail(output_size)
				img5.save(self.image5.path)
	def __str__(self):
		return f'{self.product_id}'

class ProductSize(models.Model):
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	size = models.CharField(max_length=20)
	quantity = models.IntegerField(default=0, null=True)

class ProductReview(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	review = models.TextField()
	time = models.DateTimeField(auto_now=True)

class WholeSaleProduct(models.Model):
	SEX_CHOICES = (("Male",'Male'),("Female",'Female'),("All",'All'))
	product_id = models.BigAutoField(primary_key=True)
	product_name = models.CharField(max_length=100 , default="")
	prod_seller = models.CharField(max_length=100, default="")
	category = models.ForeignKey(category, default="", verbose_name="Category", on_delete=models.SET_DEFAULT)
	subcategory = models.CharField(max_length=50, default="")
	price = models.IntegerField(default=0)
	desc = models.TextField()
	size = models.TextField(verbose_name='Size Avialabe(Separated by Comma)')
	color = models.TextField(verbose_name='Enter Color Separated by Comma')
	min_Quantity = models.IntegerField(default=0, null=True)
	pub_date = models.DateField(auto_now=True)
	image1 = models.ImageField(upload_to='products/images', default="",null=True)
	image2 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image3 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image4 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)
	image5 = models.ImageField(upload_to='products/images', default="",null=True,blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img1 = Image.open(self.image1.path)
		if img1.height > 1500 or img1.width > 1500:
			output_size = (1500, 1500)
			img1.thumbnail(output_size)
			img1.save(self.image1.path)
		if self.image2:
			img2 = Image.open(self.image2.path)
			if img2.height > 1500 or img2.width > 1500:
				output_size = (1500, 1500)
				img2.thumbnail(output_size)
				img2.save(self.image2.path)

		if self.image3:
			img3 = Image.open(self.image3.path)
			if img3.height > 1500 or img3.width > 1500:
				output_size = (1500, 1500)
				img3.thumbnail(output_size)
				img3.save(self.image3.path)

		if self.image4:
			img4 = Image.open(self.image4.path)
			if img4.height > 1500 or img4.width > 1500:
				output_size = (1500, 1500)
				img4.thumbnail(output_size)
				img4.save(self.image4.path)

		if self.image5:
			img5 = Image.open(self.image5.path)
			if img5.height > 1500 or img5.width > 1500:
				output_size = (1500, 1500)
				img5.thumbnail(output_size)
				img5.save(self.image5.path)
	def __str__(self):
		return f'{self.product_id}'

class WholeSaleProductOrders(models.Model):
	STATUS_CHOICES = (("Accepted",'Accepted'),("On The Way",'On The Way'),("Delivered",'Delivered'),("Cancel",'Cancel'))
	order_id = models.CharField(max_length=50,default='')
	user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
	products = models.CharField(max_length=50)
	status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='')

class dow(models.Model):
	product = models.OneToOneField(Product, default="", verbose_name="Product Id", on_delete=models.CASCADE, null=True)
	price = models.PositiveIntegerField()
	def __str__(self):
		return f'{self.product}'

class trend(models.Model):
	product = models.OneToOneField(Product, default="", on_delete=models.CASCADE, null=True)
	number = models.PositiveIntegerField()
	def __str__(self):
		return f'{self.product}'

class MyCart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product_id = models.CharField(max_length=100)
	number = models.PositiveIntegerField(default=0)

class Orders(models.Model):
	STATUS_CHOICES = (("Accepted",'Accepted'),("On The Way",'On The Way'),("Delivered",'Delivered'),("Cancel",'Cancel'))
	order_id = models.CharField(max_length=50,default='')
	saler = models.CharField(max_length=100,default='lokolingo@admin',)
	user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
	products = models.CharField(max_length=50)
	size = models.CharField(max_length=50,default='',null=True)
	status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='')
