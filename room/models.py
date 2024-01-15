from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug=models.CharField(unique=True,max_length=255)
    student=models.ForeignKey(User,related_name="student_room",on_delete=models.DO_NOTHING,blank=True,null=True)
    tutor=models.ForeignKey(User,related_name="tutor_room",on_delete=models.DO_NOTHING,blank=True,null=True)
    
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    
class Message(models.Model):
    room= models.ForeignKey(Room,related_name="messages",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE)
    content = models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ("date_added",)
    
    