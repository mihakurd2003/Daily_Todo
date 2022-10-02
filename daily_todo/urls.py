"""daily_todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),

    #Todos
    path('', views.home, name='home'),
    path('create/', views.create_todos, name='create_todos'),
    path('current/', views.current_todos, name='current_todos'),
    path('completed/', views.completed_todos, name='completed_todos'),
    path('current/<int:todo_id>', views.see_todo, name='see_todo'),
    path('current/<int:todo_id>/complete', views.complete_todo, name='complete_todo'),
    path('current/<int:todo_id>/delete', views.delete_todo, name='delete_todo'),
    path('current/<int:todo_id>/restore', views.restore_todo, name='restore_todo'),

]
