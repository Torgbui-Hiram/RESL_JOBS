from django.urls import path
from . import views

urlpatterns = [
    # path('register_user', views.register_user, name='register'),
    path('login_into', views.access_granting, name='granted'),
    path('logout', views.logout_user, name='logout'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
