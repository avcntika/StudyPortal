from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Notes(models.Model): #first, we create this DB table. which is then bound to the forms page. and then the forms page is connected into the views.
    user = models.ForeignKey(User, on_delete=models.CASCADE) # when user is deleted, their notes will also get deleted from DB
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Notes"


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = "Homework"

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "To Do List"


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Class = models.CharField(max_length=100)
    lectures_conducted = models.CharField(max_length=10)
    lectures_attended = models.CharField(max_length=10)
    attendance_percentage = models.CharField(max_length=10)


    def __str__(self):
        return self.Class

    class Meta:
        verbose_name_plural = "Attendance"
