from django.shortcuts import render
from markdown2 import markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        list_entry = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title, "list_entry": markdown(list_entry)
        })        
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title, "list_entry": title+"<h4>Entry not found</h4>"
        })

def search(request):
    # lookup list of entries
    entries = util.list_entries()
    query = request.POST.get('q')

    # check if list of entries contains query
    if query in entries:
        query = util.get_entry(query)
        return render(request, "encyclopedia/entry.html", {
            "title": query, "list_entry": markdown(query)
        })  