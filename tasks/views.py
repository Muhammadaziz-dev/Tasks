from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            tasks = Task.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by('priority')
        else:
            tasks = Task.objects.all().order_by('priority')

        paginator = Paginator(tasks, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'tasks': page_obj,
            'is_paginated': paginator.num_pages > 1,
            'page_obj': page_obj,
            'paginator': paginator,
            'query': query,
        }
        return render(request, 'tasks/task_list.html', context)

class TaskCreateView(LoginRequiredMixin, View):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks:task_list')
        return render(request, self.template_name, {'form': form})

class TaskUpdateView(LoginRequiredMixin, View):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        form = self.form_class(instance=task)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
        return render(request, self.template_name, {'form': form})

class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        return render(request, 'tasks/task_confirm_delete.html', {'task': task})

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect('tasks:task_list')
