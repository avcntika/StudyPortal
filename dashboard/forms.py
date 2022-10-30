from django import forms
from django.contrib.auth.forms import UserCreationForm

from . models import *

class NotesForm(forms.ModelForm): # to convert a model into a a form
    class Meta:
        model = Notes
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject','title', 'description','due', 'completed']

class DashboardForm(forms.Form): #common for all search tabs
    text = forms.CharField(max_length=200, label="Enter your search:")

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'completed']



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance

        fields = ['Class','lectures_conducted', 'lectures_attended']