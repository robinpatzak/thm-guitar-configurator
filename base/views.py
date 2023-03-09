from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySerializer, ItemSerializer, ConfigurationItemSerializer, ConfigurationSerializer, OrderItemSerializer, OrderSerializer
from django.http import JsonResponse


def home(request):
    if request.user.is_authenticated and request.method == 'POST':
        for item in request.POST:
            if item != 'csrfmiddlewaretoken':
                chosen_item = get_object_or_404(Item, id=request.POST.get(item, ""))
                configuration_item, created = ConfigurationItem.objects.get_or_create(item=chosen_item, customer=request.user.customer)

                print(request.POST.get(item, ""))
        # for item in request.POST.items():
        #     configuration_item, created = ConfigurationItem.objects.get_or_create(item=item, customer=request.user.customer)

    items = Item.objects.all()
    categories = Category.objects.all()
    max_steps = categories.count()
    configuration_items = [
        Item.objects.filter(category=1),
        Item.objects.filter(category=2),
        Item.objects.filter(category=3),
        Item.objects.filter(category=4),
        Item.objects.filter(category=5),
        Item.objects.filter(category=6),
        Item.objects.filter(category=7)
    ]

    order = []
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer=request.user.customer, is_completed=False)
        except ObjectDoesNotExist:
            order = []
    context = {
        'items': items,
        'order': order,
        'categories': categories,
        'max_steps': max_steps,
        'configuration_items': configuration_items
    }
    return render(request, 'base/home.html', context)

def configurator(request):
    guitar_models = Item.objects.filter(category=1)
    configuration_items = [
        Item.objects.filter(category=2),
        Item.objects.filter(category=3),
        Item.objects.filter(category=4),
        Item.objects.filter(category=5),
        Item.objects.filter(category=6),
        Item.objects.filter(category=7)
    ]

    context = {
        'guitar_models': guitar_models,
        'configuration_items': configuration_items
    }
    return render(request, 'base/configurator/configurator.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    
    context = {}
    return render(request, 'base/account/login.html', context)

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            user_name = register_form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user_name)
            return redirect('login')
    else:
        register_form = RegisterForm()
    
    context = {
        'register_form': register_form,
    }
    return render(request, 'base/account/register.html', context)

@login_required(login_url='login')
def account(request):
    if request.method == 'POST':
        update_user_form = UpdateUserForm(request.POST, instance=request.user)
        update_customer_form = UpdateCustomerForm(request.POST, instance=request.user.customer)
        if update_user_form.is_valid() and update_customer_form.is_valid():
            update_user_form.save()
            update_customer_form.save()
            user = update_user_form.cleaned_data.get('username')
            messages.success(request, 'Account informations changed for ' + user)
            return redirect('account')
    else:
        update_user_form = UpdateUserForm(instance=request.user)
        update_customer_form = UpdateCustomerForm(instance=request.user.customer)

    context = {
        'update_user_form': update_user_form,
        'update_customer_form': update_customer_form,
    }
    return render(request, 'base/account/account.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')
    
def add_to_cart(request, item_id, *args, **kwargs):
    item = get_object_or_404(Item, id=item_id)
    order_item, created = OrderItem.objects.get_or_create(item=item, customer=request.user.customer)
    order = Order.objects.filter(customer=request.user.customer, is_completed=False)
    if order.exists():
        if order[0].items.filter(item__id=item.id, order__customer=request.user.customer).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This items quantity was updated")
        else:
            order[0].items.add(order_item)
            messages.info(request, "This item was added to your cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(customer=request.user.customer, date_ordered=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect('home')

def remove_from_cart(request, item_id, *args, **kwargs):
    item = get_object_or_404(Item, id=item_id)
    order = Order.objects.filter(customer=request.user.customer, is_completed=False)
    if order.exists():
        if order[0].items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(item=item)[0]
            order_item.delete()
            messages.info(request, "This item was removed to your cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('home')
    else:
        messages.info(request, "User does not have an order")
        return redirect('home')
    return redirect('home')
    

# Django rest_framework 

@api_view(['GET', 'POST'])
def category_list(request, format=None):

    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def item_list(request, format=None):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def model_list(request, format=None):
    if request.method == 'GET':
        models = Item.objects.filter(category = 1)
        serializer = ItemSerializer(models, many=True)
        return Response(serializer.data)    

class ItemList(APIView):
    def get(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

def order_list(request, format=None):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return JsonResponse(serializer.data, safe=False)

def orderItem_list(request, format=None):
    orderItems = OrderItem.objects.all()
    serializer = OrderItemSerializer(orderItems, many=True)
    return JsonResponse(serializer.data, safe=False)

def configuration_list(request, format=None):
    configurations = Configuration.objects.all()
    serializer = ConfigurationSerializer(configurations, many=True)
    return JsonResponse(serializer.data, safe=False)

def configurationItem_list(request, format=None):
    configurationItems = ConfigurationItem.objects.all()
    serializer = ConfigurationItemSerializer(configurationItems, many=True)
    return JsonResponse(serializer.data, safe=False)