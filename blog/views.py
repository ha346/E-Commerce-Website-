from django.shortcuts import render
from django.http import HttpResponse 
from .models import BlogPost
# Create your views here.

def index(request):
    # return HttpResponse("Blog Index")
    myposts=BlogPost.objects.all()
    print("MYPOSTS: ",myposts)
    return render(request,"blog/index.html",{'myposts':myposts})

def blogpost(request,id): 
    post=BlogPost.objects.filter(post_id=id)[0]
    print("POSTS: ",post)
    return render(request,"blog/blogpost.html",{'post':post})

def post(request):
    return render(request,"blog/post.html")

def submitPost(request):  
    if request.method=="POST":
        heading=request.POST['heading']
        title=request.POST['title']
        content=request.POST['content'] 
        author=request.POST['author'] 
        thumbnail=request.FILES['thumbnail'] 
        if len(heading)<5 or len(title)<10 or len(content)<10 or len(author)<5:
            return render(request,"blog/post.html",{"warning":True})
        else:
            post=BlogPost(heading=heading, title=title, content=content, author=author, thumbnail=thumbnail)
            post.save() 
            return render(request,"blog/post.html",{"success":True})
    return render(request,"blog/post.html")

 
