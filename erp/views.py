from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    return render(request, 'erp/admin_dashboard.html')

@login_required
def vendedor_dashboard(request):
    return render(request, 'erp/vendedor_dashboard.html')

@login_required
def almacen_dashboard(request):
    return render(request, 'erp/almacen_dashboard.html')