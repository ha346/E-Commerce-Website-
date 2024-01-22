from django.db import models
from django.utils.timezone import now

# Create your models here.

# class BlogPost(models.Model):
#     post_id=models.AutoField(primary_key=True)
#     title=models.CharField(max_length=50,default="")
#     head0=models.CharField(max_length=500,default="")
#     chead0=models.CharField(max_length=5000,default="")
#     head1=models.CharField(max_length=50,default="")
#     chead1=models.CharField(max_length=5000,default="")
#     head2=models.CharField(max_length=50,default="")
#     chead2=models.CharField(max_length=5000,default="")
#     pub_date=models.DateField()
#     thumbnail=models.ImageField(upload_to='blog/images',default="")
    
#     def __str__(self):
#         return self.title 
    

class BlogPost(models.Model): 
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=300,default="")
    content=models.CharField(max_length=5000,default="")
    author=models.CharField(max_length=50,default="")
    heading=models.CharField(max_length=130,default="")
    pub_date= models.DateTimeField(default=now) 
    thumbnail=models.ImageField(upload_to='blog/images',default="")
    
    def __str__(self):
        return self.title + ' by ' + self.author
