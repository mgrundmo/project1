from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import markdown
from random import randint

from . import util

def index(request):
    # display of all available entries
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

    # receive search query from form 
    query = request.POST.get('q')

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
        if new_title.casefold() in entries_lwr:
            error_msg = new_title + " - this entry is already available"
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
    # get current entry to be edit and send to edit page
    title = request.POST.get('edit')
    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit.html",{
        "title": title, "entry": entry
    })

def update(request):
    # safe entry to file (overwrites excisting file)
    title = request.POST.get('title')
    entry = request.POST.get('text')
    with open("entries/%s.md" % title, "w") as file_for_update:
        file_for_update.write(entry)
    list_entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title, "list_entry": markdown(list_entry)
    })   

def random(request):
    # request list of all titles in database
    titles = util.list_entries()
    # create random number by using length of list
    rndm = randint(0, (len(titles)- 1))
    # identify title using the random number
    random_title = titles[rndm]
    # get text entry asocoiated with the title 
    random_entry = util.get_entry(random_title)
    # display random entry
    return render(request, "encyclopedia/entry.html", {
        "title": random_title, "list_entry": markdown(random_entry)
    })