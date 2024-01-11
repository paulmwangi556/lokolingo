from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import Group



    

class UserDetail(models.Model):
    SEX_CHOICES = (("Male", 'Male'), ("Female", 'Female'), ("Other", 'Other'))
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,related_name='userdetails') 
    rate_per_hour = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    profile_description=models.TextField()
    tutoring_experience=models.IntegerField(default=0,blank=True,null=True)
    country = models.CharField(max_length=100,default="Kenya")
    identification_document = models.FileField(upload_to="tutor_documents")
    photo = models.FileField( upload_to='tutor_photos')
    mobile = models.CharField(max_length=10, null=True)
    alternate_mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True)

class StudentDetails(models.Model):
    
    TUTORING_FORMAT=[
        ("one on one","One on One"),
        ("group","Group"),
       ( "flexible","Flexible")
    ]
    PRIVACY=[
        ("Share my details with matched tutors","Share my details with matched tutors"),
        ("Remain anonymous untill matching","Remain anonymous untill matching")
    ]
    
    contact_number=models.CharField(max_length=50)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    subjects=models.TextField(verbose_name="Subjects/Topics needing assistance")
    grade_level=models.CharField(max_length=100,blank=True,null=True)
    preferred_tutoring_format=models.CharField(max_length=50,choices=TUTORING_FORMAT)
    availability = models.TextField(verbose_name="Prefered Days and Times",blank=True,null=True)
    duration_per_session=models.CharField(max_length=100)
    budget_range=models.CharField(max_length=100,blank=True,null=True)
    payment_method=models.CharField(max_length=10,blank=True,null=True)
    languages_preference=models.CharField(max_length=100,blank=True,null=True)
    qualifications_desired=models.CharField(max_length=100,blank=True,null=True)
    accept_terms=models.BooleanField(default=False,verbose_name="Accept Terms and Conditions")
    privacy_preference=models.CharField(max_length=100,choices=PRIVACY)
    
    

class TutorUserDetails(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    TEACHING_MODE=[
        ("one on one",'One on One'),
        ("group sessions",'Group Sessions')
    ]
    
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="tutordetails",primary_key=True)
    contact_number=models.CharField(max_length=30,null=True,blank=True)
    profile_picture=models.FileField(upload_to="tutor_images",verbose_name="Upload A Professional Headshot")
    
    highiest_qualification=models.CharField(max_length=200,blank=True,null=True)
    specialization=models.TextField()
    years_of_experience = models.CharField(max_length=10)
    
    
    teaching_style=models.TextField()
    teaching_philosophy=models.TextField(blank=True,null=True)
    
    availability = models.CharField(max_length=50,choices=DAYS_OF_WEEK)
    preferred_teaching_method=models.CharField(max_length=50,choices=TEACHING_MODE)
    
    hourly_rate=models.CharField(max_length=50)
    preferred_payment_method=models.TextField()
    
    education_materials_link=models.TextField(blank=True,null=True)
    
    
    languages_spoken=models.CharField(max_length=100)
    cv = models.FileField(upload_to="cvs",blank=True,null=True)
    
    special_certificate_skills=models.TextField(blank=True,null=True)
    # special_certificate_files=models.FileField(upload_to="special_certs")
    
    # cancellation_policy=models.TextField(blank=True,null=True)
    terms_acceptance=models.BooleanField(default=False)
    
    
    
    def get_days_list(self):
        return self.days.split(',')

class CertificateFile(models.Model):
    tutor_user_details = models.ForeignKey(TutorUserDetails, on_delete=models.CASCADE, related_name='special_certificate_files')
    file = models.FileField(upload_to="special_certs")


class TutorRating(models.Model):
    rating = models.IntegerField()
    review = models.CharField(max_length=200)
    tutor = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="tutor")
    student=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="student")
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)


class Slider(models.Model):
    name = models.CharField(max_length=50, default="", null=True)
    image = models.ImageField(upload_to='slider_img')
    url = models.CharField(max_length=200, default="#", null=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 1024 or img.width > 1024:
            output_size = (1024, 1024)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100)
    product_size = models.CharField(max_length=20, default='', null=True)
    number = models.PositiveIntegerField(default=0)


class Contact(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email
