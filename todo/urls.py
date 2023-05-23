from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs', views.add_job, name='add_job'),
    path('job-details/<id>', views.view_details, name='job_info'),
    path('action', views.sub_action, name='status'),
    path('reminder', views.reminder, name='mail'),
]
