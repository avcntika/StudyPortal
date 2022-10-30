from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    #notes
    path('notes', views.notes, name='notes'),
    path('delete_notes/<int:pk>/', views.delete_notes, name='delete-notes'),
    path('view_notes/<int:pk>/', views.view_notes.as_view(), name='view-notes'),

    #homework
    path('homework', views.homework, name='homework'),
    path('update_homework/<int:pk>/', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>/', views.delete_homework, name='delete-homework'),

    #youtube
    path('youtube', views.youtube, name='youtube'),

    #to do list
    path('todo', views.todo, name='todo'),
    path('update_todo/<int:pk>/', views.update_todo, name='update-todo'),
    path('delete_todo/<int:pk>/', views.delete_todo, name='delete-todo'),

    #books
    path('books', views.books, name='books'),



    # attendance
    path('attendance', views.attendance, name='attendance'),
    path('update_attendance/<int:pk>/', views.update_attendance, name='update_attendance'),
    path('delete_attendance/<int:pk>/', views.delete_attendance, name='delete_attendance'),

]