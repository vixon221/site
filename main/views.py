from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Category, Dish, Restaurant

# --- Главная страница ---
def index(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(is_available=True)
    
    query = request.GET.get('q')
    if query:
        dishes = dishes.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    category_id = request.GET.get('category')
    if category_id:
        dishes = dishes.filter(category_id=category_id)

    # Подсчет количества товаров в корзине
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    # Рестораны для полноширинного блока внизу
    restaurants = Restaurant.objects.all()

    context = {
        'categories': categories,
        'dishes': dishes,
        'selected_category': int(category_id) if category_id else None,
        'search_query': query or '',
        'cart_count': cart_count,
        'restaurants': restaurants,
    }
    return render(request, 'main/index.html', context)

# --- Список заведений / 2GIS ---
def restaurants_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'main/restaurants.html', {'restaurants': restaurants})

# --- Логика Корзины ---
def add_to_cart(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    cart[dish_id_str] = cart.get(dish_id_str, 0) + 1
    request.session['cart'] = cart
    messages.success(request, "Товар добавлен в корзину!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for dish_id, quantity in cart.items():
        dish = get_object_or_404(Dish, id=dish_id)
        item_total = dish.price * quantity
        total_price += item_total
        cart_items.append({
            'dish': dish,
            'quantity': quantity,
            'total': item_total
        })

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})
    dish_id_str = str(dish_id)
    if dish_id_str in cart:
        del cart[dish_id_str]
        request.session['cart'] = cart
        messages.info(request, "Товар удален из корзины.")
    return redirect('cart')

# --- Оформление заказа и Симуляция оплаты ---
def checkout(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '')
        if len(card_number) != 16 or not card_number.isdigit():
            messages.error(request, "Введите корректный 16-значный номер карты!")
            return redirect('checkout')

        request.session['cart'] = {}
        messages.success(request, f"Оплата картой *{card_number[-4:]} прошла успешно! Заказ оформлен.")
        return redirect('home')
    
    cart = request.session.get('cart', {})
    total_price = 0
    for dish_id, quantity in cart.items():
        dish = get_object_or_404(Dish, id=dish_id)
        total_price += dish.price * quantity

    return render(request, 'main/checkout.html', {'total_price': total_price})

# --- Подписка "FoodHub Pass" ---
def subscription_view(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '')
        if len(card_number) != 16 or not card_number.isdigit():
            messages.error(request, "Введите корректный 16-значный номер карты!")
            return redirect('subscription')
            
        messages.success(request, f"Подписка FoodHub Pass успешно активирована! С карты *{card_number[-4:]} списано 490 сом.")
        return redirect('home')
        
    return render(request, 'main/subscription.html')

# --- Авторизация ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"С возвращением, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('home')
        else:
            messages.error(request, "Ошибка при регистрации.")
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('home')