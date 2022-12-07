from django.contrib import admin
from .models import Buyer,Cart

# Register your models here.
@admin.register(Buyer)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','mobile','email','password','gender','address','pic','dob']
    
    
@admin.register(Cart)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','product','buyer','quantity']