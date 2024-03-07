from django.urls import path
from . import views

# create views and then add the views pages to the path
urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.pets_list, name='pets_list'),
    path('pets/create/', views.pet_create, name='pet_create'),
    path('search/', views.search_results, name='search_results'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('pets_detail/<int:pk>/', views.pets_detail, name='pets_detail'),
    path('add_to_cart/pet/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('proceed_to_pay/', views.proceed_to_pay, name='proceed_to_pay'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('register/', views.register, name='register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('edit_pet/<int:id>', views.edit_pet, name='edit_pet'),
    path('service/', views.service_page, name='service_page'),
]