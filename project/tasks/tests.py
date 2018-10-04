# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, Client, RequestFactory

from tasks.models import Task
from tasks.views import RegisterFormView, TasksViewList, TaskCreate, mark_done


class PageTestCase(TestCase):
    c = Client()

    def setUp(self):
        self.user1 = User.objects.create_user(username='test1@example.com', email='test1@example.com', password='test1')
        self.user1_task1 = Task.objects.create(opened=self.user1, title='test1', description='Description of test1')
        self.user1_task2 = Task.objects.create(opened=self.user1, title='test2', description='Description of test2')
        self.user1_task3 = Task.objects.create(opened=self.user1, title='test3', description='Description of test3')

        self.user2 = User.objects.create_user(username='test2@example.com', email='test2@example.com', password='test2')
        self.user2_task1 = Task.objects.create(opened=self.user2, title='test4', description='Description of test4')
        self.user2_task2 = Task.objects.create(opened=self.user2, title='test5', description='Description of test5')
        self.user2_task3 = Task.objects.create(opened=self.user2, title='test6', description='Description of test6')

        self.factory = RequestFactory()
        self.anon_user = AnonymousUser()

    def test_user_signin_valid_credentials(self):
        request = self.factory.get('/sign-in/')
        request.user = self.user1
        response = RegisterFormView()
        self.assertEqual(response.response_class.status_code, 200)

    def test_show_task_list(self):
        request = self.factory.get('/')
        request.user = self.user1
        response = TasksViewList()
        self.assertEquals(response.response_class.status_code, 200)

        request.user = self.anon_user
        response = TasksViewList()
        self.assertEquals(response.response_class.status_code, 200)

    def test_user_cannot_edit_not_owned_task(self):
        request = self.factory.post('/tasks/mark/')
        request.user = self.user1
        response = mark_done(request, self.user2_task1.pk)
        self.assertEquals(response.status_code, 302)

    def test_anon_user_cannot_edit_not_owned_task(self):
        request = self.factory.post('/tasks/mark/')
        request.user = self.anon_user
        response = mark_done(request, self.user2_task1.pk)
        self.assertEquals(response.status_code, 302)
