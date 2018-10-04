# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView

from tasks.forms import RegistrationForm, TaskForm
from tasks.models import Task


class TasksViewList(ListView):
    context_object_name = 'task_list'
    template_name = 'task_list.html'

    def get_queryset(self):
        hide = self.request.GET.get('hide', None)
        filter_kw = {}
        if hide:
            filter_kw = {'completed': False}
        queryset = Task.objects.filter(**filter_kw).order_by('pk')
        return queryset


class RegisterFormView(FormView):
    form_class = RegistrationForm
    template_name = 'user_form.html'

    def get_success_url(self):
        if reverse('sign-in') or reverse('login') in self.request.META.get('HTTP_REFERER'):
            return reverse('task_list')
        return self.request.META.get('HTTP_REFERER', reverse('task_list'))

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.username = new_user.email = form.cleaned_data['email']
        new_user.save()

        login(self.request, new_user)

        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'user_form.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginFormView, self).form_valid(form)

    def get_success_url(self):
        if reverse('sign-in') or reverse('login') in self.request.META.get('HTTP_REFERER'):
            return reverse('task_list')
        return self.request.META.get('HTTP_REFERER', reverse('task_list'))


def logout_user(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', reverse('task_list')))


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super(TaskCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_task = form.save(commit=False)
        new_task.opened = self.request.user
        new_task.save()
        return super(TaskCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('task_list')


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def test_func(self):
        return self.get_object().opened == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super(TaskUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('task_list')


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    form_class = TaskForm
    template_name = 'confirm_delete_task.html'

    def test_func(self):
        return self.get_object().opened == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super(TaskDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('task_list')


@login_required
def mark_done(request, pk):
    task_obj = get_object_or_404(Task, pk=pk)
    task_obj.completed = True
    task_obj.closed = request.user
    task_obj.save()

    return redirect(reverse('task_list'))
