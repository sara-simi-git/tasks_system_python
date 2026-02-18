from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_func),
    path("login/", views.login_func,name='login'),
    path("register/", views.register_func,name='register'),
    path("tasks/tasks_list/", views.tasks_list, name='tasks_list'),
    path("tasks/delete/<int:id>/", views.delete_task, name='delete_task'),
    path("tasks/edit_task/<int:id>/", views.edit_task, name='edit_task'),
    path("tasks/add_task/", views.add_task, name='add_task'),
    path("tasks/change_status/<int:id>/", views.change_status, name='change_status')
]