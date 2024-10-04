from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import markdown

from . import util

import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title",max_length=100)
    content = forms.CharField(label="Content",widget=forms.Textarea)
    
class EditPageForm(forms.Form):
    content = forms.CharField(label="Content",widget=forms.Textarea)

def index(request):
    
    query = request.GET.get('q'," ").strip()# Obtener y limpiar el valor de búsqueda
    entries = util.list_entries()
    
    if query: #if exist query
        if query in entries: #si query esta en entries
            return redirect('entry_page',title=query) #Redirige la entrada de la pagina
        
        # Filtrar las entradas que contienen la consulta como subcadena
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
         
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries,
            "query": query
        })
    
    return render(request, "encyclopedia/index.html", {
    "entries": entries
    })
    
def entry_page(request,title):
    entry = util.get_entry(title)
    if entry:
        entry_html = markdown(entry)
        return render(request, f"encyclopedia/entry.html", {
            "entry":  entry_html,
            "title": title.capitalize()
        }) 
    else:
        raise Http404(f"The page {title} does not exist.")
    
def edit_entry(request,title):

    entry = util.get_entry(title)
    if entry is None:
        raise Http404(f"The page {title} does not exist.")
    if request.method== "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"] # Obtener el contenido
            util.save_entry(title,new_content)
            return redirect("get_entry",title)
    else:
        form = EditPageForm(initial={"content":entry})
            
    return render(request, f"encyclopedia/edit_entry.html", {
            "entry": entry,
            "title": title.capitalize(),
            "form":form
        }) 
          
def new_page(request):
    
    form = NewPageForm()

    if request.method== "POST":
        form = NewPageForm(request.POST) # Crear el formulario con datos POST
        if form.is_valid():
            title = form.cleaned_data["title"].strip() # Obtener y limpiar el título
            content = form.cleaned_data["content"] # Obtener el contenido
            
            # Verificar si ya existe una entrada con el mismo título
            if util.get_entry(title): #si existe el titulo nuevo redirigimos a la pagina con un error
                return render(request,"encyclopedia/new_page.html",{
                "form": form,
                "error": "The page already exist."
            })
                        
            util.save_entry(title,content)
            return redirect("get_entry",title) # Redirigir a la nueva entrada
        
        else:
            form = NewPageForm() # Mostrar un formulario vacío
              
    return render(request,"encyclopedia/new_page.html",{
        "form": form
    })    
    
def random_page(request):   
    
    entries_list = util.list_entries()
    if not entries_list:
        raise Http404("No entries available.")
    random_entry = random.choice(entries_list)
    entry = util.get_entry(random_entry)
    if entry is None:
        raise Http404(f"The page {random_entry} does not exist.")
    return redirect("get_entry",title=random_entry) 
    





