from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import Tasks
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

# Create your views here.

class StartingPageView(View):
    def get(self, request):
        is_logged_in = request.user.is_authenticated
        if is_logged_in:
            added_tasks = Tasks.objects.filter(user=request.user)
            user = request.user
        else:
            added_tasks = request.session.get("guest_tasks", [])
            user = None
        return render(request, "my_list/index.html", {
            "is_logged_in": is_logged_in,
            "tasks" : added_tasks,
            "user" : user,
        })
    
    def post(self, request):
        task = request.POST["new_task"]
        if request.user.is_authenticated:
            new_task_entry = Tasks(task=task, user=request.user)
            new_task_entry.save()
        else:
                if 'guest_tasks' not in request.session:
                    request.session['guest_tasks'] = []
                    
                new_task = {
                    'id': len(request.session['guest_tasks']) + 1,
                    'task': task,
                    'is_done': False,
                    'date': timezone.now().strftime("%Y-%m-%d %H:%M"),
                }
            
                request.session['guest_tasks'].append(new_task)
                request.session.modified = True
        return HttpResponseRedirect(reverse("home-page"))


class RegisterPageView(View):
    def get(self, request):
        return render(request, "my_list/register.html")
    
    def post(self, request):
        user_name = request.POST["username"]
        user_email = request.POST["email"]
        user_password = request.POST["password"]
        new_user = User.objects.create_user(
            username=user_name,
            email=user_email,
            password=user_password
        )
        login(request, new_user)
        return HttpResponseRedirect(reverse("home-page"))
    
class LoginPageView(View):
    def get(self, request):
        return render(request, "my_list/login.html")
    
    def post(self, request):
        user_name = request.POST["user_name"]
        user_password = request.POST["user_password"]
        user = authenticate(request, username=user_name, password=user_password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home-page"))
        else:
            return HttpResponseRedirect(reverse("login-user"))

 
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("home-page"))
    
class DeleteView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            task = Tasks.objects.get(pk=id)
            if task:
                task.delete()
        else:
            guest_tasks = request.session.get("guest_tasks", [])
            guest_tasks = [task for task in guest_tasks if task["id"] != int(id)]
            request.session["guest_tasks"] = guest_tasks
            request.session.modified = True
        return HttpResponseRedirect(reverse("home-page"))
    
class MarkDoneView(View):
    def post(self, request, id):
        if request.user.is_authenticated:
            task = get_object_or_404(Tasks, pk=id, user=request.user)
            if not task.is_done:
                task.is_done = True
                task.save()
        else:
            guest_tasks = request.session.get("guest_tasks", [])
            for task in guest_tasks:
                if task['id'] == int(id):
                    task["is_done"] = True
                    break
            request.session["guest_tasks"] = guest_tasks
            request.session.modified = True
        return HttpResponseRedirect(reverse("home-page"))


