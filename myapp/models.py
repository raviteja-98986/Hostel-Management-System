from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm

# Create your models here.
class Room(models.Model):
    room_no=models.IntegerField(primary_key=True)
    floor=models.IntegerField()
    sharing=models.IntegerField()

    def check_availability(self):
        if self.pk:
            return True  # allow updates
        return self.room.available_beds() > 0
    @property
    def available_slots(self):
        total_members = self.person_set.count()
        return self.sharing - total_members

    def available_beds(self):
        return self.sharing - self.person_set.count()

    def __str__(self):
        return f"{self.room_no}"

class Person(models.Model):
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    address=models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} {self.room}"

    def save(self, *args, **kwargs):
     # Allow updates without blocking
        if not self.pk:
            if self.room.available_beds() <= 0:
                raise ValidationError("Room is full!")

        super().save(*args, **kwargs)
class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'age', 'address']

