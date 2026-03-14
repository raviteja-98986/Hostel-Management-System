from collections import defaultdict

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Room, Person, PersonForm

def is_admin(user):
    return user.is_superuser

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

def login_option(request):
    return render(request, 'myapp/login_option.html')

def login_admin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "This portal is for admins only.")
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/admin_login.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_superuser:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Admins must use the Admin portal.")
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/user_login.html', {'form': form})

def index(request):
    return render(request,template_name='index.html')

@login_required
def Rooms(request):
    rooms = Room.objects.all().order_by('floor', 'room_no')

    floor_dict = defaultdict(list)

    for room in rooms:
        floor_dict[room.floor].append(room)

    return render(request, "myapp/Rooms.html", {"rooms": dict(floor_dict)})
    return render(request,template_name='myapp/Rooms.html',context={'rooms':floor_dict})
def Home(request):
    return render(request,template_name='myapp/Home.html')
@login_required
def Room_members(request, room_no):
    room = Room.objects.get(room_no=room_no)
    persons = Person.objects.filter(room=room)
    return render(request, template_name='myapp/Room_members.html', context={'room': room, 'persons': persons})
@login_required
def Room_details(request, room_no):
    room = Room.objects.get(room_no=room_no)
    persons = Person.objects.filter(room=room)
    return render(request, template_name='myapp/Room_details.html', context={'room': room, 'persons': persons})


@login_required
@user_passes_test(is_admin)
def Add_person(request, room_no):
    room = get_object_or_404(Room, room_no=room_no)
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.room = room
            person.save()
            return redirect('room_details', room_no=room.room_no)
    else:
        form = PersonForm()

    return render(request, "myapp/Person_form.html", {"form": form, "room": room})

@login_required
@user_passes_test(is_admin)
def Delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    room_no = person.room.room_no
    person.delete()
    return redirect('room_details', room_no=room_no)

@login_required
@user_passes_test(is_admin)
def Change_room(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    old_room = person.room
    # Get all rooms with available slots
    # We use a list comprehension or filter based on sharing and person_set count
    all_rooms = Room.objects.all()
    available_rooms = [r for r in all_rooms if r.available_slots > 0 or r == person.room]
    
    if request.method == "POST":
        new_room_no = request.POST.get('room_no')
        new_room = get_object_or_404(Room, room_no=new_room_no)
        person.room = new_room
        person.save()
        return redirect('room_details', room_no=old_room)

    return render(request, "myapp/Change_room.html", {
        "person": person,
        "available_rooms": available_rooms
    })

@login_required
@user_passes_test(is_admin)
def Edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    room = person.room
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('room_details', room_no=room.room_no)
    else:
        form = PersonForm(instance=person)

    return render(request, "myapp/Edit_person.html", {"form": form, "person": person})
