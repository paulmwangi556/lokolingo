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
