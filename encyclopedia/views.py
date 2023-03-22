from django.http import HttpResponse
from django.shortcuts import render
from . import util


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