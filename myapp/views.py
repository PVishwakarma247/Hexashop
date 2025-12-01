from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
User = get_user_model()
from decimal import Decimal
from django.core.paginator import Paginator



# Create your views here.

def home(request):
    menproduct = Product.objects.filter(category=Product.CATEGORY_MENS)
    womenproduct = Product.objects.filter(category=Product.CATEGORY_WOMENS)
    kidsproduct = Product.objects.filter(category=Product.CATEGORY_KIDS)
    messages.info(request, 'Use Desktop for better experience')
    return render(request, 'myapp/index.html', {'menproduct': menproduct, 'womenproduct': womenproduct, 'kidsproduct': kidsproduct})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('home')

def login_view(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not User.objects.filter(email=email).exists():
                messages.warning(request, "Invalid User")
                return redirect('signup')
            
            user = authenticate(email=email, password=password)
            if user is None:
                messages.warning(request, "Invalid Credentials")
                return redirect('login_view')
            else:
                login(request, user)
                request.session['email'] = email
                messages.success(request, "Login Successful")
                return redirect('home')
    except Exception as e:
        print(e)
    return render(request, 'myapp/login.html')

def signup(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(email=email).exists():
                messages.info(request, "Already Register")
                return redirect('login_view')
            
            user = User.objects.create(
                address=address,
                mobile=phone,
                email=email,
            )
            user.set_password(password)
            user.save()
            messages.success(request, "Registration Successful")
            return redirect('login_view')
    except Exception as e:
        print(e)
    return render(request, 'myapp/signup.html')

def about(request):
    try:
        if request.user.is_authenticated:
            return render(request, 'myapp/about.html')
        else:
            return redirect('login_view')
    except Exception as e:
        print(e)
        return redirect('login_view')

def contact(request):
    try:
        if request.user.is_authenticated:
            return render(request, 'myapp/contact.html')
        else:
            return redirect('login_view')
    except Exception as e:
        print(e)
        return redirect('login_view')


def product(request):
    try:
        if request.user.is_authenticated:
            # Paginate products: 9 per page
            products_qs = Product.objects.all().order_by('-id')
            paginator = Paginator(products_qs, 9)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'myapp/products.html', {'page_obj': page_obj})
        else:
            return redirect('login_view')
    except Exception as e:
        print(e)
        return redirect('login_view')
    
def product_details(request, category, product_id):
    if category not in {Product.CATEGORY_MENS, Product.CATEGORY_WOMENS, Product.CATEGORY_KIDS}:
        return HttpResponse("Invalid Category", status=404)

    product = get_object_or_404(Product, id=product_id, category=category)
    return render(request, 'myapp/single_product.html', {'product': product, 'category': category})


def add_to_cart(request):
    # Handle POST from single_product add-to-cart form
    try:
        if request.method != 'POST':
            return redirect('home')

        if not request.user.is_authenticated:
            messages.info(request, 'Please login to add items to cart')
            return redirect('login_view')

        user = request.user

        category = request.POST.get('category')
        product_id_raw = request.POST.get('product_id')

        # normalize quantity safely
        try:
            quantity = int(request.POST.get('quantity') or 1)
            if quantity < 1:
                quantity = 1
        except (TypeError, ValueError):
            quantity = 1

        # validate category
        if category not in {Product.CATEGORY_MENS, Product.CATEGORY_WOMENS, Product.CATEGORY_KIDS}:
            messages.info(request, 'Invalid product category')
            return redirect('product')

        # Resolve product: prefer numeric id filtered by category
        if not product_id_raw:
            messages.info(request, 'No product specified')
            return redirect('product')

        product = None
        try:
            product_pk = int(product_id_raw)
            product = get_object_or_404(Product, pk=product_pk, category=category)
        except (ValueError, TypeError):
            # not numeric, try name lookup within category
            try:
                product = Product.objects.get(name=product_id_raw, category=category)
            except Product.DoesNotExist:
                messages.info(request, 'Product not found')
                return redirect('product')

        cart, _ = Cart.objects.get_or_create(user=user)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            item.quantity = item.quantity + quantity
            item.save()

        messages.success(request, f'Added {quantity} x {product.name} to your cart')
        return redirect('cart')
    except Exception as e:
        print('add_to_cart error:', e)
        messages.warning(request, 'Could not add item to cart')
        return redirect('product')


def update_cart_item(request, item_id):
    """Increment or decrement a CartItem's quantity. Expects POST with op='inc' or op='dec' or op='set' and optional 'quantity'."""
    try:
        if request.method != 'POST':
            return redirect('cart')

        if not request.user.is_authenticated:
            messages.info(request, 'Please login to modify cart')
            return redirect('login_view')

        user = request.user
        item = get_object_or_404(CartItem, id=item_id, cart__user=user)

        op = request.POST.get('op')
        if op == 'inc':
            item.quantity += 1
            item.save()
        elif op == 'dec':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                # remove if would go to zero
                item.delete()
        elif op == 'set':
            qty = int(request.POST.get('quantity') or 1)
            if qty <= 0:
                item.delete()
            else:
                item.quantity = qty
                item.save()

        return redirect('cart')
    except Exception as e:
        print('update_cart_item error:', e)
        messages.info(request, 'Could not update cart item')
        return redirect('cart')


def remove_cart_item(request, item_id):
    try:
        if request.method != 'POST':
            return redirect('cart')

        if not request.user.is_authenticated:
            messages.info(request, 'Please login to modify cart')
            return redirect('login_view')

        user = request.user
        item = get_object_or_404(CartItem, id=item_id, cart__user=user)
        item.delete()
        messages.success(request, 'Item removed from cart')
        return redirect('cart')
    except Exception as e:
        print('remove_cart_item error:', e)
        messages.info(request, 'Could not remove item')
        return redirect('cart')

def cart(request):
    try:
        if request.user.is_authenticated:
            user = request.user

            cart = Cart.objects.filter(user=user).first()
            if cart:
                items = list(cart.items.select_related('product').all())
            else:
                items = []

            # compute line totals and subtotal
            subtotal = Decimal('0.00')
            for it in items:
                line = (it.product.price or Decimal('0.00')) * it.quantity
                # attach a convenient attribute for template
                it.line_total = line
                subtotal += line

            shipping = Decimal('10.00') if subtotal > 0 else Decimal('0.00')
            total = subtotal + shipping

            context = {
                'cart_items': items,
                'subtotal': "{:.2f}".format(subtotal),
                'shipping': "{:.2f}".format(shipping),
                'total': "{:.2f}".format(total),
            }

            return render(request, 'myapp/cart.html', context)
        else:
            return redirect('login_view')
    except Exception as e:
        print(e)
        return redirect('login_view')