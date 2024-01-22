from django.urls import path 
from . import views
urlpatterns = [ 
    path('',views.index,name="blogHome"), 
    path('post/',views.post,name="post"), 
    path('submitpost',views.submitPost,name="postblog"), 
    path('blogpost/<int:id>',views.blogpost,name="blogPost") 
] 