from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home,name="home"),
    path('home', views.Home,name="home"),
    path('rooms',views.Rooms,name='rooms'),
    path('room_details/<int:room_no>',views.Room_details,name='room_details'),
    # path('room/<int:room_no>',views.Room_members,name="room_members"),
]