from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, user_passes_test

from project import settings
from tasks import views


urlpatterns = [
    url(r'^sign-in/$', views.RegisterFormView.as_view(), name='sign-in'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^tasks/create/$', views.TaskCreate.as_view(), name='create-task'),
    url(r'^tasks/(?P<pk>[\d-]+)/edit/$', views.TaskUpdate.as_view(), name='edit-task'),
    url(r'^tasks/(?P<pk>[\d-]+)/delete/$', views.TaskDelete.as_view(), name='delete-task'),
    url(r'^tasks/(?P<pk>[\d-]+)/mark/$', views.mark_done, name='mark_done'),
    url(r'^', views.TasksViewList.as_view(), name='task_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
