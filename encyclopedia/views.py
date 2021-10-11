from typing import Pattern
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
import re
import random
from django import forms

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="New Entry")
    content = forms.CharField(label="Entry Definition", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "content": util.get_entry(entry),
        "title": entry
    })

def search(request):
    search_text = request.GET['q']
    entries = util.list_entries()

    matches = []

    for entry in entries:
        if search_text.lower() == entry.lower():
            return redirect('entry', entry)
        else:
            match = re.search(rf"{search_text}".lower(), entry.lower())       
            if match:
                matches.append(entry)
    
    return render(request, "encyclopedia/search.html", {"entries": matches})

def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if title in util.list_entries():
                return render(request, "encyclopedia/create.html", {"message":"Entry already exists."})
            util.save_entry(title, content)

        else:
            return render(request, "encyclopedia/create.html", {"form":form})

    return render(request, "encyclopedia/create.html", {"form":EntryForm})
    
def edit(request, title):   
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('entry', title)
        else:
            return render(request, "encyclopedia/create.html", {"form":form})

    form = EntryForm({"title":title, "content":util.get_entry(title)})
    return render(request, "encyclopedia/edit.html", {"form":form})

def random_entry(request):
    entries = util.list_entries()
    print(entries)
    entry = random.choice(entries)
    print(entry)

    return redirect('entry', entry)

   


