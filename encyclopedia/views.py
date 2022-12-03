from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    entry_md = util.get_entry(title)
    if entry_md == None:
        return render(request, "encyclopedia/404.html", {"message": "Page not found."})
    else:
        entry_html = Markdown().convert(entry_md)
        content = {
            "title": title,
            "entry": entry_html,
        }
        return render(request, "encyclopedia/entry.html", content)

def search(request):
    key = request.POST.get('q')
    if not key:
        return HttpResponseRedirect(reverse("index"))
    
    entry_list = util.list_entries()
    entry_list_now = []
    if key in entry_list:
        return HttpResponseRedirect(reverse("entry",args=(key,)))
    else:
        for entry in entry_list:
            if entry.find(key) != -1:
                entry_list_now.append(entry)
        content = {
            "entries": entry_list_now
        }
        return render(request, "encyclopedia/search.html", content)
    
def random(request):
    entry_list = util.list_entries()
    num = randint(0, len(entry_list)-1)
    return HttpResponseRedirect(reverse("entry", args=(entry_list[num],)))

def  create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title: 
            return render(request,"encyclopedia/404.html")
        elif not content:
            return render(request,"encyclopedia/404.html")
        else:
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"encyclopedia/create.html")
    
def edit(request, title):
    entry_md = util.get_entry(title)
    if entry_md == None:
        return render(request,"encyclopedia/404.html")
    elif request.method == 'GET':
        content = {
            "title":title,
            "entry":entry_md,
        }
        return render(request, "encyclopedia/edit.html", content)
    else:
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("index"))