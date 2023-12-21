from datetime import datetime
from pickle import NONE
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CommentForm
from .forms import BlogForm
from .models import Product, Cart, CartItem
from .forms import CartItemForm
from .models import Blog
from django.http import JsonResponse
from .models import Comment
from django.shortcuts import render, redirect, get_object_or_404



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Страница с нашими контактами.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Сведения о нас.',
            'year': datetime.now().year,
        }
    )


def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )


def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year': datetime.now().year,
        }
    )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )


def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {'1': 'Каждый день', '2': 'Несколько раз в день',
                '3': 'Несколько раз в неделю', '4': 'Несколько раз в месяц'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['internet'] = internet[form.cleaned_data['internet']]
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['emil'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form': form,
            'data': data
        }
    )


def registration(request):
    """Renders the registration page."""

    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False  # запрещен вход в административный отдел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            regform.save()  # сохраняем изменения после добавления полей
            return redirect('home')  # переадресация на главную старницу после регистарции
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )


def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )


def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео',
            'year': datetime.now().year,
        }
    )


def product_list(request):
    products = Product.objects.all()
    return render(request, 'app/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = CartItemForm()

    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.subtotal = cart_item.product.price * cart_item.quantity
            cart_item.save()
            cart.total_price += cart_item.subtotal
            cart.save()

    return render(request, 'app/product_deta0il.html', {'product': product, 'form': form})


def view_cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = cart.total_price
    return render(request, 'app/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    print("Received request to add to cart.")
    product = get_object_or_404(Product, pk=product_id)
    form = CartItemForm(request.POST or None)

    if form.is_valid():
        print("Form is valid.")
        quantity = form.cleaned_data['quantity']
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)


        if not created:
            cart_item.quantity += quantity
            cart_item.subtotal = cart_item.product.price * cart_item.quantity
            cart_item.save()

        cart.total_price += cart_item.subtotal
        cart.save()

        print(f"Product {product.name} added to the cart. Total price: {cart.total_price}")

    response_data = {'total_price': cart.total_price}
    return JsonResponse(response_data)


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    Cart.objects.filter(pk=cart.pk).update(total_price=F('total_price') - cart_item.subtotal)

    cart_item.delete()

    return redirect('app:view_cart')


def update_cart(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')

        print(f"Updating cart item {cart_item_id} with quantity {quantity}")

        cart_item = get_object_or_404(CartItem, pk=cart_item_id)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity should be a positive integer.")
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'})

        cart_item.quantity = quantity
        cart_item.subtotal = cart_item.product.price * cart_item.quantity
        cart_item.save()

        # Обновляем общую стоимость корзины
        update_cart_total(cart_item.cart)


        return JsonResponse({
            'new_quantity': cart_item.quantity,
            'total_price': cart_item.cart.total_price,
        })
    else:
        return HttpResponse('Invalid request', status=400)

def update_cart_total(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.subtotal for item in cart_items)
    Cart.objects.filter(pk=cart.pk).update(total_price=total_price)


@login_required
def get_cart_contents(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        cart_items = []

    return render(request, 'app/view_cart.html', {'cart_items': cart_items})

