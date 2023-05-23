from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('auth/', include('members.urls')),
    # path('auth/', include('django.contrib.auth.urls')),
]
