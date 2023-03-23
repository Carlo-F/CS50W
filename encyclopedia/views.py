from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from . import util

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry title")
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
        "title": entry.title,
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
            #finally redirect user to the new entry page
            return HttpResponseRedirect(reverse("entry", args=[entry_title]))
    else:
        return render(request, "encyclopedia/new_entry.html",{
            "form": NewEntryForm()
        })