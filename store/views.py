from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Order, OrderItem


def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        
        if not username or not password:
            messages.error(request, "Username & Password required")
            return redirect('register')

       
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account Created Successfully ✅")
        return redirect('login')

    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":

        logout(request)   # ⭐ VERY IMPORTANT LINE

        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('staff_products')
            else:
                return redirect('products')

        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'login.html')

@login_required
def staff_products(request):

    if not request.user.is_staff:
        return redirect('products')

    data = Product.objects.all()

    return render(request, 'staff_products.html', {'data': data})


@login_required
def add_product(request):

    if not request.user.is_staff:
        return redirect('products')

    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            description=request.POST.get("description"),
            image=request.FILES.get("image")
        )
        return redirect('staff_products')

    data = Product.objects.all()

    return render(request, 'staff_products.html', {
        'show_add_form': True,
        'data': data
    })


@login_required
def edit_product(request, id):

    if not request.user.is_staff:
        return redirect('products')

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        return redirect('staff_products')

    data = Product.objects.all()

    return render(request, 'staff_products.html', {
        'edit_product': product,
        'data': data
    })


@login_required
def delete_product(request, id):

    if not request.user.is_staff:
        return redirect('products')

    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('staff_products')


@login_required
def products(request):
    data = Product.objects.all()
    return render(request, 'products.html', {'data': data})


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')

@login_required
def buy_now(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'buy_now.html', {'product': product})


@login_required
def place_order(request, id):

    product = get_object_or_404(Product, id=id)

    order = Order.objects.create(
        user=request.user,
        username=request.user.username,
        total_amount=product.price
    )

    OrderItem.objects.create(
    order=order,
    product=product,
    product_name=product.name,   
    quantity=1,
    price=product.price
)

    return render(request, 'buy_now.html', {
        'success': f"{product.name} Ordered Successfully ✅"
    })


@login_required
def buy_cart(request):

    items = Cart.objects.filter(user=request.user)

    if not items:
        return redirect('cart')

    total = 0
    for i in items:
        total += i.product.price * i.quantity

   
    order = Order.objects.create(
        user=request.user,
        username=request.user.username,
        total_amount=total
    )

    
    for i in items:
        OrderItem.objects.create(
    order=order,
    product=i.product,
    product_name=i.product.name,   
    quantity=i.quantity,
    price=i.product.price
)

    
    items.delete()

    return render(request, 'buy_now.html', {
        'success': "Order Placed Successfully ✅"
    })


@login_required
def cart(request):

    items = Cart.objects.filter(user=request.user)

    total = 0
    for i in items:
        total += i.product.price * i.quantity

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })
from .models import Profile

@login_required
def profile(request):

    profile_obj, created = Profile.objects.get_or_create(
        user_id=request.user.id   
    )

    if request.method == "POST":
        profile_obj.address = request.POST.get("address")
        profile_obj.mobile = request.POST.get("mobile")

        if request.FILES.get("image"):
            profile_obj.image = request.FILES.get("image")

        profile_obj.save()

    return render(request, "profile.html", {"profile": profile_obj})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def increase_qty(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_qty(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


@login_required
def remove_item(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart')