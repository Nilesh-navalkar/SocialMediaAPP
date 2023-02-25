from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
user=get_user_model()
# Create your models here.
class profile(models.Model):
    u=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.TextField()
    email=models.EmailField()
    def __str__(self):
        return self.email

class bio(models.Model):
    u=models.ForeignKey(user,on_delete=models.CASCADE)
    un=models.TextField(default="xxxxxxxxxxxxxxxxxxx")
    b=models.TextField(default="")
    name=models.TextField(default="anon")
    country=models.TextField(default="wonderland")
    phone=models.IntegerField(default="0000000000")
    dob=models.DateField(default="2000-01-01")
    profilepic=models.ImageField(upload_to='pimages/',default="d.png")
    def __str__(self):
        return self.u.username

class post(models.Model):
    u=models.ForeignKey(user,on_delete=models.CASCADE)
    s=models.TextField(default='admin')
    newpost=models.ImageField(upload_to="uploads")
    t=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.u.username

class follow(models.Model):
    u=models.TextField()
    f=models.TextField()
    def __str__(self):
        return self.u

    
    
