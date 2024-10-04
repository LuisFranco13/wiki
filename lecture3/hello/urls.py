from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("<str:name>",views.greet,name="greet"),
    path("luis",views.luis,name="luis"),
    path("person",views.person,name="person"),
    
]