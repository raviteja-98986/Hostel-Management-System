from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home,name="home"),
    path('home', views.Home,name="home"),
    path('rooms',views.Rooms,name='rooms'),
    path('room_details/<int:room_no>',views.Room_details,name='room_details'),
    path('add_person',views.Add_person,name="add_person"),
    path('remove_person/<int:person_id>',views.Remove_person,name="remove_person"),
    path('room/<int:room_no>', views.Room_members, name="room_members"),
]