from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    list_entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "list_entry": list_entry
    })
