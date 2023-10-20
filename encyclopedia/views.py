import random
import markdown2

from django import forms
from django.shortcuts import render

from . import util

class NewQueryForm(forms.Form):
   query=forms.CharField(label="")

class NewEntryForm(forms.Form):
   titulo=forms.CharField(label="Titulo",required=False,
                         widget= forms.TextInput
                           (attrs={
                               'class': 'clsTitulo',
                               'name': 'titulo',
                               'placeholder':'Ingrese el título de la entrada',
                               'required': 'True'
                            }))
   entrada=forms.CharField(label="Contenido",required=False,
                           widget=forms.Textarea(
                            attrs={
                               'class': 'clsEntrada',
                               'name': 'entrada',
                               'placeholder':'Ingrese el detalle de la entrada',
                               'required': 'True'
                            }  
                           ))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "formQuery": NewQueryForm
    })

title=""

def entrys(request,title):
    buscar=util.get_entry(title)

    if buscar:
       return render(request, "encyclopedia/entries.html", {
        "getEntry": markdown2.markdown(util.get_entry(title)),
        "title": title
        })
    else:
       return render(request, "encyclopedia/404.html")     

def query(request):
    if request.method == "POST":
       form = NewQueryForm(request.POST)

       if form.is_valid():
          query=form.cleaned_data["query"]

          buscar=util.get_entry(query)

          if buscar:
            return render(request, "encyclopedia/query.html", {
                "getEntry": util.get_entry(query),
                "title": query
                })
          else:
            return render(request, "encyclopedia/query.html", {
                "entries": util.query_entries(query)
                })   
       else:
            return render(request, "encyclopedia/index.html", {
                "formQuery": form
                })              
       
def newEntry(request):
    form = NewEntryForm(request.POST)
    
    if request.method == "POST":
       if form.is_valid():
          titulo=form.cleaned_data["titulo"]
          entrada=form.cleaned_data["entrada"]

          buscar=util.get_entry(titulo)
          msgError=""
         
          if buscar:
             msgError="La entrada '"+titulo+"' ya existe."

             return render(request, "encyclopedia/newEntry.html", {
                "getError": msgError,
                "formCreate": form
                }) 
          else:
             try:
                crear=util.save_entry(titulo,entrada)
                
                return render(request, "encyclopedia/entries.html",{
                   "getEntry": util.get_entry(titulo),
                   "title": titulo
                }) 
             except Exception as err:
                msgError=f"Unexpected {err=}, {type(err)=}"

                return render(request, "encyclopedia/newEntry.html", {
                "getError": msgError,
                "formCreate": form
                }) 
    else:
        return render(request, "encyclopedia/newEntry.html", {
        "formCreate": form
    })

def edit(request,title):
    form = NewEntryForm(request.POST)

    if request.method == "POST":
       if form.is_valid():
          entrada=form.cleaned_data["entrada"]    

          try:
             crear=util.save_entry(title,entrada)
                
             return render(request, "encyclopedia/entries.html",{
                   "getEntry": util.get_entry(title),
                   "title": title
             }) 
          
          except Exception as err:
            msgError=f"Unexpected {err=}, {type(err)=}"

            return render(request, "encyclopedia/edit.html", {
            "formEdit": util.get_entry(title),
            "title": title,
            "getError": msgError
            })                 
    else:
       buscar=util.get_entry(title)
         
       if buscar:
          return render(request, "encyclopedia/edit.html", {
          "formEdit": util.get_entry(title),
          "title": title
          })
       else:
          return render(request, "encyclopedia/404.html")   
       
def randomQuery(request):
    lista=util.list_entries()
    aleatorio=random.choice(lista)
    return entrys(request,aleatorio)