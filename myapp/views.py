from collections import defaultdict

from django.shortcuts import render
from .models import Room,Person

def index(request):
    return render(request,template_name='index.html')

def Rooms(request):
    rooms = Room.objects.all().order_by('floor', 'room_no')

    floor_dict = defaultdict(list)

    for room in rooms:
        floor_dict[room.floor].append(room)

    return render(request, "myapp/Rooms.html", {"rooms": dict(floor_dict)})
    return render(request,template_name='myapp/Rooms.html',context={'rooms':floor_dict})
def Home(request):
    return render(request,template_name='myapp/Home.html')
# def Room_members(request,room_no):
#     persons = Person.objects.filter(room__room_no=room_no)
#     return render(request,template_name='myapp/Room_members.html',context={'persons':persons})
def Room_details(request,room_no):
    persons=Person.objects.filter(room=room_no)
    return render(request,template_name='myapp/Room_details.html',context={'persons':persons})

