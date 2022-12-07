from django.contrib import admin
from .models import Seller,Product

# Register your models here.
@admin.register(Seller)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','mobile','email','password','gender','pic','dob']
    
@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','name','des','price','quantity','pic']
