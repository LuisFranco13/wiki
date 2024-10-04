from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>",views.entry_page,name="get_entry"),
    path("<str:title>/edit",views.edit_entry,name="edit_entry"),
    path('new_page/', views.new_page, name='new_page'),    
    path('random/', views.random_page, name='random_page'),
]

