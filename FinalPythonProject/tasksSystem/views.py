from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.db import transaction


def login_func(request):
    if request.method == "POST":
        id = request.POST['id']
        password = request.POST['password']
        u = User.objects.filter(id=id, password=password).first()
        if not u:
            return redirect('login')
        else:
            request.session['user'] = {"id": u.id, "fullName": u.fullName, "isAdmin": u.isAdmin, "teamId": u.team.id,
                                       "teamName": u.team.name}
            return HttpResponseRedirect("/tasks/tasks_list/")
    else:
        form = login()
    return render(request, "login.html", {"form": form})


def register_func(request):
    if request.method == "POST":
        id = request.POST['id']
        fullName = request.POST['fullName']
        password = request.POST['password']
        phone = request.POST['phone']
        teamArr = request.POST['team'].split('. ')
        team = Team(teamArr[0], teamArr[1])
        teamHeadAvailable = True
        for u in User.objects.all():
            if u.team_id == int(teamArr[0]) and u.isAdmin is True:
                teamHeadAvailable = False
                break
        if fullName[0:8] == 'teamhead' and teamHeadAvailable is True:
            isAdmin = True
        else:
            isAdmin = False
        u = User(id=id, fullName=fullName, password=password, phone=phone, team=team, isAdmin=isAdmin)
        u.save()
        request.session['user'] = {"id": u.id, "fullName": u.fullName, "isAdmin": u.isAdmin, "teamId": u.team.id,
                                   "teamName": u.team.name}
        return HttpResponseRedirect("/tasks/tasks_list/")
    else:
        teams = Team.objects.all()
    return render(request, "register.html", {"teams": teams})


def tasks_list(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    tasks = Task.objects.filter(team_id=user['teamId'])
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    user_id = request.GET.get('user_id')
    if user_id:
        tasks = tasks.filter(user_id=user_id)
    users = User.objects.filter(team_id=user['teamId'])
    return render(request, 'tasks_list.html', {'list': tasks, 'user': user, 'users': users})


def edit_task(request, id):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    task = get_object_or_404(Task, pk=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form})


def delete_task(request, id):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    task = get_object_or_404(Task, pk=id)
    if request.method == "POST":
        task.delete()
        return redirect('tasks_list')

    return render(request, 'tasks_list/tasks_list.html')


@transaction.atomic
def add_task(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.team_id = user['teamId']
            task.save()
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


def change_status(request, id):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    task = get_object_or_404(Task, pk=id)
    if request.method == "POST":
        if task.status == 'new':
            task.user_id = user['id']
            task.status = 'in proccess'
        else:
            task.status = 'finish'
        task.save()
    return redirect('tasks_list')
