import uuid

from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=50, unique="true")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    def __str__(self):
        return self.username


class Posts(models.Model):
    title = models.CharField(max_length=20,default=uuid.uuid4,unique=True)
    description = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="posts")
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now="true")
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title



class Comments(models.Model):
    text = models.CharField(max_length=100)
    writer_id = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)





class UserDetails(models.Model):
    user= models.OneToOneField(User,on_delete= models.CASCADE)
    profile_picture = models.ImageField(upload_to="profiles",default="imgs/usericonblue.png")


    mobile = models.CharField(max_length=10,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)




