from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Prefetch
from django.urls import reverse
from core.apps.singer.forms import UserRegistrationForm

from django.views.generic import ListView, DetailView, CreateView
from core.apps.singer.models import Task, Category
from core.apps.minor.models import UserTaskEnroll, UserAnswers, FavouriteTask, Drugs

from core.apps.singer.forms import TaskCreateForm, CategoryCreateForm


# register and login

class UserRegistrationView(CreateView):

    form_class=UserRegistrationForm
    template_name="task/register.html"
    context_object_name="form"

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Ошибка регистрации')
            return render(request, self.template_name, {'form': form})


class TaskDetailView(DetailView): # open task

    #model=Task
    queryset=Task.objects.select_related("category").all()
    template_name="task/index2.html"
    context_object_name="task"
    pk_url_kwarg="task_id"


    def create_like(self, task_id):

        task = Task.objects.get(pk=task_id)
        print(task)

        task.cnt_likes += 1
        task.save(update_fields=["cnt_likes"])

        new = FavouriteTask.objects.create(user=self.request.user, task=task)
        new.save()

        return HttpResponseRedirect(self.request.META["HTTP_REFERER"])

    def delete_like(self, task_id):

        task = Task.objects.get(pk=task_id)

        task.cnt_likes -= 1
        task.save(update_fields=["cnt_likes"])

        new = FavouriteTask.objects.get(user=self.request.user, task=task)
        new.delete()

        return HttpResponseRedirect(self.request.META["HTTP_REFERER"])


    def create_bm(self, task_id):

        task = Task.objects.get(pk=task_id)

        task.cnt_bm += 1
        task.save(update_fields=["cnt_bm"])

        new = Drugs.objects.create(user=self.request.user, task=task)
        new.save()

        return HttpResponseRedirect(self.request.META["HTTP_REFERER"])

    def delete_bm(self, task_id):

        task = Task.objects.get(pk=task_id)

        task.cnt_bm -= 1
        task.save(update_fields=["cnt_bm"])

        new = Drugs.objects.get(user=self.request.user, task=task)
        new.delete()

        return HttpResponseRedirect(self.request.META["HTTP_REFERER"])   


class TaskListViews(ListView): # open all tasks

    model=Task
    template_name="task/index.html"
    context_object_name="tasks"

    def get_queryset(self) -> QuerySet[Task]:

        q = Task.objects.prefetch_related(
            Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=self.request.user).select_related("user")),
            Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=self.request.user)),
            Prefetch("savedtasks", queryset=Drugs.objects.filter(user=self.request.user))
        ).select_related("category").all()

        return list(q)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная'

        return context


class CategoryListViews(ListView):
    
    model=Task
    template_name="task/index.html"
    context_object_name="tasks"

    def get_queryset(self) -> QuerySet[Task]:

        q = super().get_queryset().filter(
            category_id=self.kwargs['category_id']
        ).prefetch_related(
            Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=self.request.user).select_related("user")),
            Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=self.request.user)),
            Prefetch("savedtasks", queryset=Drugs.objects.filter(user=self.request.user))
        ).select_related("category").all()

        return q
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context["title"] = 'другая недогланая'

        return context

class HistoryListViews(ListView):

    model=Task
    template_name="task/index.html"
    context_object_name="tasks"

    def get_queryset(self) -> QuerySet[Task]:

        queryset=Task.objects.filter(
            useranswers__user=self.request.user
        ).prefetch_related(
            Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=self.request.user).select_related("user")),
            Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=self.request.user)),
            Prefetch("savedtasks", queryset=Drugs.objects.filter(user=self.request.user))
        ).select_related("category").all()

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context["title"] = 'совсем другая недогланая'

        return context

class FavouriteTaskListViews(ListView):

    model=Task
    template_name="task/index.html"
    context_object_name="tasks"

    def get_queryset(self) -> QuerySet[Task]:
        return super().get_queryset().filter(
            favouritetask__user=self.request.user
        ).prefetch_related(
            Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=self.request.user).select_related("user")),
            Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=self.request.user)),
            Prefetch("savedtasks", queryset=Drugs.objects.filter(user=self.request.user))
        ).select_related("category").all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context["title"] = 'совсем совсем другая недогланая'

        return context

class DrugsListViews(ListView):

    model=Task
    template_name="task/index.html"
    context_object_name="tasks"

    def get_queryset(self) -> QuerySet[Task]:
        return super().get_queryset().filter(
            savedtasks__user=self.request.user
        ).prefetch_related(
            Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=self.request.user).select_related("user")),
            Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=self.request.user)),
            Prefetch("savedtasks", queryset=Drugs.objects.filter(user=self.request.user))
        ).select_related("category").all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context["title"] = 'ну вот совсем другая недогланая'

        return context

class SeenTaskListViews(ListView):

    model=Task
    template_name="task/index.html"
    context_object_name="tasks"

    def get_queryset(self) -> QuerySet[Task]:

        q = super().get_queryset().filter(
            usertaskenroll__user=self.request.user
        ).prefetch_related(
            Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=self.request.user).select_related("user")),
            Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=self.request.user)),
            Prefetch("savedtasks", queryset=Drugs.objects.filter(user=self.request.user))
        ).select_related("category").all()

        return q
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context["title"] = 'совсем недогланая'

        return context

class LikesListViews(ListView):
    
    model=Task
    template_name="task/index.html"
    context_object_name="tasks"

    def get_queryset(self) -> QuerySet[Task]:
        return super().get_queryset().filter(
            favouritetask__user=self.request.user
        ).prefetch_related(
            Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=self.request.user).select_related("user")),
            Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=self.request.user)),
            Prefetch("savedtasks", queryset=Drugs.objects.filter(user=self.request.user))
        ).select_related("category").all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context["title"] = 'другая jkhk недогланая'

        return context

# administrator's commands

class TaskCreateView(CreateView):

    model=Task
    form_class=TaskCreateForm
    template_name="task/create.html"
    context_object_name="form"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:

        form.instance.author=self.request.user
        form.instance.save()

        return super().form_valid(form)
    
class CategoryCreateView(CreateView):

    model=Category
    form_class=CategoryCreateForm
    template_name="category/create.html"
    context_object_name="form"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:

        form.instance.save()

        return super().form_valid(form)


def index(request): #main page

    queryset = Task.objects.prefetch_related(
        Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=request.user).select_related("user"))
    ).select_related("category").all()
    for r in queryset:
        hj = r.usertaskenroll.all
        print(hj, type(hj))
    
    return render(request, "task/index.html", {'title': 'Главная', 'tasks': queryset})

def index2(request, task_id): #open task

    task = Task.objects.get(pk=task_id)

    new_try = UserAnswers.objects.create(user=request.user, task=task)
    new_try.save()

    new, created = UserTaskEnroll.objects.get_or_create(user=request.user, task=task)

    task.cnt_views += 1
    task.save(update_fields=["cnt_views"])

    new.save()

    return render(request, "task/index2.html", {'title': 'неглавная', 'task': task})

def index3(request, category_id): #list of tasks with the same category

    category = Category.objects.get(id=category_id)
    queryset = Task.objects.filter(category=category)

    return render(request, "task/index.html", {'title': 'другая недогланая', 'tasks': queryset})

def index4(request): # list of watched tasks (unique)

    queryset = Task.objects.prefetch_related(
        Prefetch("usertaskenroll", queryset=UserTaskEnroll.objects.filter(user=request.user)),
        Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=request.user)),
        Prefetch("savedtasks", queryset=Drugs.objects.filter(user=request.user))
    ).filter(usertaskenroll__user=request.user)

    print(queryset)

    return render(request, "task/index.html", {'title': 'совсем недогланая', 'tasks': queryset})

def index5(request): #history create (repeated tasks)

    queryset = Task.objects.prefetch_related(
        Prefetch("useranswers", queryset=UserAnswers.objects.filter(user=request.user)),
        Prefetch("favouritetask", queryset=FavouriteTask.objects.filter(user=request.user)),
        Prefetch("savedtasks", queryset=Drugs.objects.filter(user=request.user))
    ).filter(useranswers__user=request.user)

    print(queryset)

    return render(request, "task/index.html", {'title': 'совсем другая недогланая', 'tasks': queryset})

def index6_1(request): #likes page stupied method works incorrect :(

    queryset = FavouriteTask.objects.filter(user=request.user)
    print(queryset)
    
    return render(request, "task/index3.html", {'title': 'Главная', 'tasks': queryset})

def index6_2(request): #bookmarks page

    queryset = Drugs.objects.filter(user=request.user)
    print(queryset)
    
    return render(request, "task/i.html")#, {'title': 'Главная', 'tasks': queryset})

def watch_likes(request, task_id):
    queryset = FavouriteTask.objects.filter(task_id=task_id)
    print(queryset)
    
    return render(request, "task/index3.html", {'title': 'Главная', 'tasks': queryset})

#admin

def add_category(request):

    if request.method == "POST":
        form = CategoryCreateForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            new = Category.objects.create(
                title=form.cleaned_data["title"]
            )
            new.save()

            return redirect(reverse("add_category"))
    else:
        print('get')
        form=CategoryCreateForm()

    return render(request, "category/create.html", {'form': form})


def add_task(request):

    if request.method == "POST":

        print('post')
        form = TaskCreateForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            '''
            new = Task.objects.create(
                description=form.cleaned_data["description"],
                answer=form.cleaned_data["answer"],
                author=form.cleaned_data["author"],
                category=form.cleaned_data["category"],
                cnt_likes=form.cleaned_data["likes"])
            '''
            new = Task.objects.create(
                **form.cleaned_data,
                author=request.user,
            )
            new.save()

            return redirect(reverse("add_task"))


    else:
        print('get')
        form=TaskCreateForm()

    return render(request, "task/create.html", {'form': form})






    task = Task.objects.get(pk=task_id)

    task.cnt_bm -= 1
    task.save(update_fields=["cnt_bm"])

    new = Drugs.objects.get(user=request.user, task=task)
    new.delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])