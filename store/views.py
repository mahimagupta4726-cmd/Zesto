from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Order, OrderItem


# ─── Cart helpers ────────────────────────────────────────────────
def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def build_cart_items(cart):
    items, total = [], Decimal('0')
    for pid, data in cart.items():
        try:
            product = Product.objects.get(id=int(pid))
            sub = Decimal(str(data['price'])) * data['quantity']
            total += sub
            items.append({'product': product, 'quantity': data['quantity'], 'subtotal': sub})
        except Product.DoesNotExist:
            pass
    return items, total


# ─── Pages ──────────────────────────────────────────────────────
def home(request):
    return render(request, 'store/home.html', {
        'categories': Category.objects.all(),
        'featured':   Product.objects.filter(stock__gt=0).order_by('-created_at')[:8],
    })

def product_list(request):
    qs   = Product.objects.filter(stock__gt=0).select_related('category')
    cats = Category.objects.all()
    cat_slug = request.GET.get('category', '')
    query    = request.GET.get('q', '').strip()
    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/product_list.html', {
        'products': qs, 'categories': cats,
        'selected_category': cat_slug, 'query': query,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related': related})


# ─── Cart ────────────────────────────────────────────────────────
def cart_detail(request):
    items, total = build_cart_items(get_cart(request))
    return render(request, 'store/cart.html', {'cart_items': items, 'total': total})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart    = get_cart(request)
    pid     = str(product_id)
    qty     = max(1, int(request.POST.get('quantity', 1)))
    if pid in cart:
        cart[pid]['quantity'] += qty
    else:
        cart[pid] = {'name': product.name, 'price': str(product.price), 'quantity': qty}
    save_cart(request, cart)
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

def update_cart(request, product_id):
    cart = get_cart(request)
    pid  = str(product_id)
    qty  = int(request.POST.get('quantity', 0))
    if pid in cart:
        if qty > 0: cart[pid]['quantity'] = qty
        else:       del cart[pid]
    save_cart(request, cart)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    save_cart(request, cart)
    messages.info(request, 'Item removed from cart.')
    return redirect('cart_detail')


# ─── Checkout & Orders ───────────────────────────────────────────
@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_detail')
    items, total = build_cart_items(cart)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user, total_price=total,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
        )
        for item in items:
            OrderItem.objects.create(order=order, product=item['product'],
                                     quantity=item['quantity'], price=item['product'].price)
            item['product'].stock -= item['quantity']
            item['product'].save()
        save_cart(request, {})
        messages.success(request, f'🎉 Order #{order.id} placed successfully!')
        return redirect('order_success', order_id=order.id)

    return render(request, 'store/checkout.html', {'cart_items': items, 'total': total})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


# ─── Auth ────────────────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.username}! Your account is ready.')
        return redirect('home')
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        return redirect(request.GET.get('next', 'home'))
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('home')
