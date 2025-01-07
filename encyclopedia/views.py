from django.http import HttpResponse
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
    if request.method == "POST":
        # get new title and entry
        new_title = request.POST.get('title')
        new_entry = request.POST.get('text')

        # check if title already exists , print error mesage if yes
        list_entries = util.list_entries()
        entries_lwr = [i.lower() for i in list_entries]
        print(entries_lwr)
        print(new_title)
        if new_title.casefold() in entries_lwr:
            print("error")
            error_msg = new_title + " - this entry is already available"
            print(error_msg)
            return render(request, "encyclopedia/entry.html", {
                "error": error_msg
            })

        else:
            # create new file from title and entry
            with open("entries/%s.md" % new_title, "w") as new_file:
                new_file.write("# %s\n\n" % new_title)
                new_file.write(new_entry + "\n")
            list_entry = util.get_entry(new_title)

            # display new entry
            return render(request, "encyclopedia/entry.html", {
                "title": new_title, "list_entry": markdown(list_entry)
            })   
    else:
        return render(request, "encyclopedia/newpage.html")
    
def edit(request):
    return render(request, "encyclopedia/edit.html")