from django.urls import path
from .import views


urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('checkout/',views.checkout,name='checkout'),
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('make_payment/', views.make_payment, name="make_payment"),
    path('delect_cart_product/<int:pk>',views.delect_cart_product,name='delect_cart_product'),
    path('make_payment/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    
    
    
    
    
]