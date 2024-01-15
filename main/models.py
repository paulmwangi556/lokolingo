from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.urls import reverse

from datetime import datetime, time
    

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
    
    availability = models.CharField(max_length=100,verbose_name="General Availability")
    preferred_teaching_method=models.CharField(max_length=50,choices=TEACHING_MODE)
    
    hourly_rate=models.CharField(max_length=50)
    preferred_payment_method=models.TextField()
    
    education_materials_link=models.TextField(blank=True,null=True)
    
    
    languages_spoken=models.CharField(max_length=100)
    cv = models.FileField(upload_to="cvs",blank=True,null=True)
    
    special_certificate_skills=models.TextField(blank=True,null=True)
    special_certificate_files=models.FileField(upload_to="special_certs",blank=True,null=True)
    
    # cancellation_policy=models.TextField(blank=True,null=True)
    terms_acceptance=models.BooleanField(default=False)
    
    
    
    




class TutorRating(models.Model):
    rating = models.IntegerField()
    review = models.CharField(max_length=200)
    tutor = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="tutor")
    student=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="student")
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)


class Event(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    day=models.DateField(verbose_name="day of Event",blank=True,null=True)
    start_time=models.TimeField(verbose_name="Time",blank=True,null=True)
    end_time=models.TimeField(verbose_name="Time",blank=True,null=True)
    notes=models.TextField(verbose_name="Any Notes",blank=True,null=True)
    
    
    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        fixed_start_time = datetime.combine(datetime.today(), fixed_start)
        fixed_end_time = datetime.combine(datetime.today(), fixed_end)
        new_start_time = datetime.combine(datetime.today(), new_start)
        new_end_time = datetime.combine(datetime.today(), new_end)

        return not (new_start_time >= fixed_end_time or new_end_time <= fixed_start_time)

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=(self.id,))
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time or self.start_time is None:
            pass
        else:
            if self.end_time <= self.start_time:
                raise ValidationError("Ending times must be after starting time")

            events = Event.objects.filter(day=self.day)
            if events.exists():
                for event in events:
                    if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                        raise ValidationError(f'There is an overlap with another Event: {event.day}, {event.start_time}-{event.end_time}')
    def save(self, *args, **kwargs):
        self.clean()  # Call clean method explicitly
        super().save(*args, **kwargs)

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
