from collections import defaultdict

from django.shortcuts import redirect, render
from .models import Room,Person,PersonForm

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
def Room_members(request, room_no):
    room = Room.objects.get(room_no=room_no)
    persons = Person.objects.filter(room=room)
    return render(request, template_name='myapp/Room_members.html', context={'room': room, 'persons': persons})
def Room_details(request, room_no):
    room = Room.objects.get(room_no=room_no)
    persons = Person.objects.filter(room=room)
    return render(request, template_name='myapp/Room_details.html', context={'room': room, 'persons': persons})


def Add_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():   # correct method name
            form.save()
            return redirect('rooms')  # change to your URL name
    else:
        form = PersonForm()  # empty form for GET request

    return render(request, "myapp/Person_form.html", {"form": form})

def Remove_person(request, person_id):
    person = Person.objects.get(id=person_id)
    person.delete()
    return redirect('rooms')


