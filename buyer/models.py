from django.db import models
from seller.models import Product

# Create your models here.
class Buyer(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    address=models.TextField(max_length=200, null=True,blank=True)
    pic=models.FileField(upload_to='profile',default='sad.png')
    dob=models.DateTimeField(null=True,blank=True)
    gender=models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return str(self.id)
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete= models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self) -> str:
        return self.buyer.str(id)