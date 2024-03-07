import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q 
from .models import Pet, Cart, CartItems
from .forms import PetForm, CustomUserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.



def home(request):
    return render(request, 'petstoreapp/home.html')



def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
        
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'register.html', {'form':form})




def registration_success(request):
    return render(request, 'registration_success.html')




def pets_list(request):
    pets = Pet.objects.all()
    return render(request, 'petstoreapp/pets_list.html', {'pets': pets})



def service_page(request):
    return render(request, 'petstoreapp/service_page.html')



def edit_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pets_list')
    else:
        form = PetForm(instance=pet)
    return render(request, 'petstoreapp/edit_pet.html', {'form': form})



def pets_detail(request, pk):
    pets = get_object_or_404(Pet, pk=pk)
    return render(request, 'petstoreapp/pets_detail.html', {'pets': pets})



def add_to_cart(request, pk):
    if request.method == 'POST':
        pet = get_object_or_404(Pet, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItems.objects.get_or_create(cart=cart, pet=pet, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        return redirect('cart')



def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItems, id=cart_item_id)
    cart_item.delete()
    return redirect('cart') 
       
       
       
def cart_view(request):
    cart_items = CartItems.objects.filter(cart__user=request.user)
    return render(request, 'petstoreapp/cart.html', {'cart_items': cart_items})



def proceed_to_pay(request):
    cart_items = CartItems.objects.filter(cart__user=request.user)
    total_amount = sum(item.pet.price * item.quantity for item in cart_items)
    return render(request, 'petstoreapp/proceed_to_pay.html', {'total_amount': total_amount})



@csrf_exempt
def payment_confirmation(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItems.objects.filter(cart=cart)
    order_amount = 0
    total_amount = sum(item.pet.price * item.quantity for item in cart_items)
    client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
    order_amount = (order_amount + total_amount) * 100
    order_currency = 'INR'
    order = client.order.create({'amount':order_amount, 'currency':order_currency})
    context = {'order_amount': order_amount, 'order': order, 'razorpay_key_id': settings.RAZORPAY_TEST_KEY_ID}
    return render(request, 'petstoreapp/payment_confirmation.html', context)




def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)   
        if form.is_valid():
            form.save()
            return redirect('pets_list')
    else:
        form = PetForm()
    return render(request, 'petstoreapp/pet_create.html', {'form': form})




def search_results(request):
    search_query = request.GET.get('search', '')
    pets = Pet.objects.filter(Q(name__icontains=search_query) | Q(breed__icontains=search_query))
    return render(request, 'petstoreapp/search_results.html', {'pets': pets, 'search_query': search_query})




def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('pets_list')
        else:
            pass
    return render(request, 'petstoreapp/login.html')



def my_logout(request):
    logout(request)
    return redirect('home')