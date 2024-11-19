from django.shortcuts import render
from markdown2 import markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "header": "All Pages"
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
    # lookup list of entries and make lowercase
    entries = util.list_entries()
    entries_lwr = [i.lower() for i in entries]

    # receive search query from form and make lowercase
    query = request.POST.get('q')
    # query = query.lower()

    # check if list of entries contains query non case sensitive
    if query.casefold() in entries_lwr:
        query = util.get_entry(query)
        return render(request, "encyclopedia/entry.html", {
            "title": query, "list_entry": markdown(query)
        })  

    # check if if list of entries contains substring of query
    elif query:
        result = [search for search in entries if query.casefold() in search.casefold()]  
        return render(request, "encyclopedia/index.html", {
        "entries": result, "header": "Search Results"
        })
     
    # return to index page if query not found    
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })
    
def newpage(request):
    return render(request, "encyclopedia/newpage.html")