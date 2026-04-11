# erp/views/home.py
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from ..models import Producto

@login_required
def home(request):
    """Vista principal que redirige según el rol del usuario"""
    role = request.user.profile.role
    
    if role == 'admin':
        return redirect('erp:admin_dashboard')
    elif role == 'vendedor':
        return redirect('erp:vendedor_dashboard')
    elif role == 'almacen':
        return redirect('erp:almacen_dashboard')
    else:
        messages.error(request, 'Rol no válido')
        return redirect('login')

@login_required
def admin_dashboard(request):
    """Dashboard para administradores"""
    context = {
        'user_role': request.user.profile.role,
        'total_productos': Producto.objects.count(),
        'stock_bajo': Producto.objects.filter(stock__lte=5).count(),
        'sin_stock': Producto.objects.filter(stock=0).count(),
    }
    return render(request, 'erp/admin_dashboard.html', context)

@login_required
def vendedor_dashboard(request):
    """Dashboard para vendedores"""
    context = {
        'user_role': request.user.profile.role,
        'productos_destacados': Producto.objects.filter(stock__gt=0)[:10],
        'total_productos_disponibles': Producto.objects.filter(stock__gt=0).count(),
    }
    return render(request, 'erp/vendedor_dashboard.html', context)

@login_required
def almacen_dashboard(request):
    """Dashboard para almacén"""
    from django.db import models
    
    context = {
        'user_role': request.user.profile.role,
        'total_productos': Producto.objects.count(),
        'stock_total': Producto.objects.aggregate(total=models.Sum('stock'))['total'] or 0,
        'productos_bajo_stock': Producto.objects.filter(stock__lte=5),
    }
    return render(request, 'erp/almacen_dashboard.html', context)