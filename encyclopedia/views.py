import random
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from . import util

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry title")
    entry_content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))

class NewEditForm(forms.Form):
    entry_title = forms.CharField(label="Entry title",widget=forms.HiddenInput())
    entry_content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    page_url = "encyclopedia/404.html"

    if entry is not None:
        page_url = "encyclopedia/entry.html"
    
    return render(request, page_url, {
        "title": title.capitalize(),
        "entry": entry
    })

def search(request):
    # 1. get the q parameter
    query = request.GET.get('q', '')
    # 2. try to get entry with title=q
    entry = util.get_entry(query)
    # 3. if not found, get list of entries with q as substring, then redirect to search results page
    if entry is None:
        return render(request, "encyclopedia/search.html", {
            "entries": util.search_entry(query)
        })
    # 4. display search results page
    return render(request, "encyclopedia/entry.html", {
        "title": query,
        "entry": entry
    })

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']
            #check if entry already exists
            if(util.get_entry(entry_title)):
                #if it exists, show error
                return HttpResponse('Sorry, this entry already exists. Go back and try a different Entry Title.')
            #else save entry
            util.save_entry(entry_title,entry_content)
            #and finally redirect user to the new entry page
            return HttpResponseRedirect(reverse("entry", args=[entry_title]))
    else:
        return render(request, "encyclopedia/new_entry.html",{
            "form": NewEntryForm()
        })

def random_entry (request):
    entries = util.list_entries()

    random_entry = random.choice(entries)

    return HttpResponseRedirect(reverse("entry", args=[random_entry]))

def edit_entry (request, title):
    if request.method == "POST":
        form = NewEditForm(request.POST)

        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_content = form.cleaned_data['entry_content']

            util.save_entry(entry_title,entry_content)

            return HttpResponseRedirect(reverse("entry", args=[entry_title]))

    else:
        entry = util.get_entry(title,False)
        page_url = "encyclopedia/404.html"

        if entry is not None:
            page_url = "encyclopedia/edit_entry.html"

        initial_dict = {
            "entry_title" : title,
            "entry_content": entry
        }
        
        return render(request, "encyclopedia/edit_entry.html",{
            "title": title.capitalize(),
            "form": NewEditForm(request.POST or None, initial = initial_dict)
        })