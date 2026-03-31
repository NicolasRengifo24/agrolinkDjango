from django.shortcuts import render, redirect

# Create your views here.

def carrito_compra(request):
    return render(request, 'compra/carrito.html')
