from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        list_entry = util.get_entry(title)
    else:
        list_entry = util.get_entry("error")        
    return render(request, "encyclopedia/entry.html", {
        "title": title, "list_entry": markdown(list_entry)
    })

