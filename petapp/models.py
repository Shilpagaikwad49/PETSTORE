from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    name=models.CharField(max_length=20)
    type=models.CharField(max_length=10)
    breed=models.CharField(max_length=20)
    gender=models.CharField(max_length=6)
    age=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    details=models.CharField(max_length=30)
    pimage=models.ImageField(upload_to ='image', default=0)
    
    
class Cart(models.Model):
    # foreign key must be set as a refrence to the object
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column='pid')
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity=models.IntegerField(default=1)
 

    
class Order(models.Model):
    orderid=models.IntegerField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column='pid')
    quantity=models.IntegerField()