import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .models import Notes, Homework, ToDo, Attendance
from .forms import NotesForm, HomeworkForm, DashboardForm, ToDoForm, UserRegisterForm, AttendanceForm
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required
from django.views import generic


from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.

@login_required
def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'dashboard/home.html')

    else:

        return redirect('login')

### CREATE ###

@login_required
def notes(request):
    if request.method == 'POST': #if user wants to create new notes post
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,  #creating object 'notes'
                          title=request.POST['title'],
                          description=request.POST['description'])
            notes.save() # saves all these details inputted by user into the table/DB
        messages.success(request, f"Notes added by {request.user.username} successfully!!")

    else: #user doesnt wanna create new post, just access existing notes
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user) #'Notes' is the model. we retrieve all objects of this model from the DB. then filter according to login username passed here and the user can retreive all the notes only theyve created
    context = {'notes': notes, 'form':form}
    return render(request, 'dashboard/notes.html', context)

### DELETE ###
@login_required
def delete_notes(request, pk=None):
    Notes.objects.get(id=pk).delete() # each new note post has a unique primary key. the notes for that specific primary key will be deleted
    return redirect("notes")

### READ ###

class view_notes(DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == 'POST': #if user wants to create new Homeworks
        form = HomeworkForm(request.POST)

        if form.is_valid():
            try:
                completed = request.POST['completed']

                if completed == 'on': # if homework is completed, set boolean value as true and check the box
                    completed = True
                else:
                    completed = False

            except:
                completed = False

            homework = Homework( #creating object homework
                user=request.user, # login user
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                completed=completed #('completed' column defined in model) = ('completed' variable  defined in the try statement of this view
            )

            homework.save()
            messages.success(request, f"Homework added by {request.user.username} successfully.")

    else: #user doesnt wanna create new homework, just access existing homeworks
        form = HomeworkForm()

    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
       homework_done = True

    else:
        homework_done = False
    context = {'homeworks': homework, 'homeworks_done': homework_done, 'form': form}
    return render(request,'dashboard/homework.html',context)

@login_required
def update_homework(request, pk= None): # for checkbox
    homework = Homework.objects.get(id=pk)
    if homework.completed == True:
        homework.completed = False

    else:
        homework.completed = True

    homework.save()
    return redirect("homework")

@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete() # each new note post has a unique primary key. the notes for that specific primary key will be deleted
    return redirect("homework")


def youtube(request):
    if request.method == "POST": # if user is searching something
        form = DashboardForm(request.POST)
        text = request.POST['text'] #access the text data of the users search
        video = VideosSearch(text, limit=10)
        result_list = [] #creating an empty list to store all the results

        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'viewCount': i['viewCount']['short'],
                'publishedTime': i['publishedTime'],


            }
            desc = '' #sosme vids have descriptions and some dont. so first setting desc as an empty string
            if i['descriptionSnippet']: #if there is a description
                for j in i['descriptionSnippet']:
                    desc += j['text'] #concatenating
            result_dict['description'] = desc
            result_list.append(result_dict)

            context = {'form': form, 'results': result_list}

        return render(request, 'dashboard/youtube.html',context)

    else: #user is not searching anything, no results are showing
        form = DashboardForm()
    context={'form':form}
    return render(request, 'dashboard/youtube.html',context)

@login_required
def todo(request):
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            try:
                completed = request.POST['completed']

                if completed == 'on': # if homework is completed, set boolean value as true and check the box
                    completed = True
                else:
                    completed = False

            except:
                completed = False

            todos = ToDo(  # creating object homework
                user=request.user,  # login user
                title=request.POST['title'],
                completed=completed
                # ('completed' column defined in model) = ('completed' variable  defined in the try statement of this view
            )
            todos.save()
            messages.success(request, f"New task to be completed added by {request.user.username} .")

    else:
        form = ToDoForm()


    todo = ToDo.objects.filter(user=request.user)

    if len(todo) == 0:
        todos_done = True

    else:
        todos_done = False
    context = {"todos": todo, 'todos_done': todos_done, 'form': form}
    return render(request, 'dashboard/todo.html', context)

@login_required
def update_todo(request, pk= None): # for checkbox
    todo = ToDo.objects.get(id=pk)
    if todo.completed == True:
        todo.completed = False

    else:
        todo.completed = True

    todo.save()
    return redirect("todo")

@login_required
def delete_todo(request, pk=None):
    ToDo.objects.get(id=pk).delete() # each new note post has a unique primary key. the notes for that specific primary key will be deleted
    return redirect("todo")


def books(request):
    if request.method == "POST":  # if user is searching something
        form = DashboardForm(request.POST)
        text = request.POST['text']  # access the text data of the users search
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()


        result_list = []  # creating an empty list to store all the results

        for i in range(10):
            result_dict = {

                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),

                'categories':answer['items'][i]['volumeInfo'].get('categories '),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLinks')




            }


            result_list.append(result_dict)

            context = {'form': form, 'results': result_list}

        return render(request, 'dashboard/books.html', context)

    else: #user is not searching anything, no results are showing
        form = DashboardForm()
    context={'form':form}
    return render(request, 'dashboard/books.html',context)




def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account successfully created for {username} .")
            return redirect('login')

    else:
        form = UserRegisterForm

    context = {'form': form}
    return render(request, 'dashboard/register.html', context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(completed=False,user=request.user)
    ToDos = ToDo.objects.filter(completed=False, user=request.user)

    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    if len(ToDos) == 0:
        ToDo_done = True
    else:
        ToDo_done = False

    context = { 'homeworks': homeworks, 'ToDos': ToDos, 'homework_done': homework_done, 'ToDo_done': ToDo_done}

    return render(request, 'dashboard/profile.html', context )

@login_required()
def attendance(request):
    allAttendance = Attendance.objects.filter(user=request.user)
    form = AttendanceForm()
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            lectures_conducted = request.POST['lectures_conducted']
            lectures_attended = request.POST['lectures_attended']
            attendPerct = (int(lectures_attended)/int(lectures_conducted))*100
            print(attendPerct)
            Attendance.objects.create(user=request.user,
                                      Class=request.POST['Class'],
                                      lectures_conducted=request.POST['lectures_conducted'],
                                      lectures_attended=request.POST['lectures_attended'],
                                      attendance_percentage=attendPerct)

            return redirect('attendance')
    context = {'attendances': allAttendance, 'form': form}
    return render(request,'dashboard/attendance.html',context)

@login_required()
def update_attendance(request, pk):
    MyData = Attendance.objects.get(id=pk)
    UpdateForm = AttendanceForm(request.POST or None, instance=MyData) #to fetch data of a particular project from the db into the update form
    if UpdateForm.is_valid():
        UpdateForm.save(commit=False)
        MyData.Class = request.POST['Class']
        MyData.lectures_conducted = request.POST['lectures_conducted']
        MyData.lectures_conducted = request.POST['lectures_attended']
        MyData.save()
        return redirect('attendance')
    context = {"form": UpdateForm}
    return render(request, 'dashboard/update_attendance.html', context)



@login_required()
def delete_attendance(request, pk=None):
    Attendance.objects.get(id=pk).delete() # each new note post has a unique primary key. the notes for that specific primary key will be deleted
    return redirect("attendance")
