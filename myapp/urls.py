from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home,name="home"),
    path('home', views.Home,name="home"),
    path('rooms',views.Rooms,name='rooms'),
    path('room_details/<int:room_no>',views.Room_details,name='room_details'),
    path('add_person/<int:room_no>',views.Add_person,name="add_person"),
    path('delete_person/<int:person_id>',views.Delete_person,name="delete"),
    path('room/<int:room_no>', views.Room_members, name="room_members"),
    path('change_room/<int:person_id>', views.Change_room, name="change_room"),
    path('edit_person/<int:person_id>', views.Edit_person, name="edit_person"),
    path('signup/', views.signup, name='signup'),
    path('login_option/', views.login_option, name='login_option'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('login_user/', views.login_user, name='login_user'),
]