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
