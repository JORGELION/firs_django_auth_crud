from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('productos/', views.productos, name="productos"),
    path('contactenos/', views.contactenos, name="contactenos"),
    path('login/', views.iniciosesion, name="login"),
    path("signup/", views.registrarse, name="signup"),
    path("logout/", views.cerrarsesion, name="logout"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/complete", views.complete_task, name="complete_task"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="delete_task"),
    path("tasks_completed/", views.tasks_completed, name="tasks_completed"),
]
