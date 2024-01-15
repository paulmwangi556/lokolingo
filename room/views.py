from django.shortcuts import render

from . import models
from django.contrib.auth.decorators import login_required
# Create your tests here.

@login_required
def rooms(request):
    rooms = models.Room.objects.all()
    
    return render(request, 'room/rooms.html', {'rooms':rooms})


@login_required
def room(request,id):
    room =models.Room.objects.get(id=id)
    messages = models.Message.objects.filter(room=room)[0:25]
    return render(request, 'room/room.html', {'room':room,"messages":messages})
    
    