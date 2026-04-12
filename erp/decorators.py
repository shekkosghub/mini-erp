# erp/decorators.py
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

def role_required(allowed_roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles permitidos.
    
    Uso:
    @role_required(['admin', 'almacen'])
    def mi_vista(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied('Debes iniciar sesión')
            
            user_role = request.user.profile.role
            if user_role not in allowed_roles:
                raise PermissionDenied('No tienes permiso para acceder a esta sección')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(view_func):
    """Decorador específico para admin"""
    return role_required(['admin'])(view_func)

def almacen_required(view_func):
    """Decorador específico para almacén"""
    return role_required(['almacen'])(view_func)

def admin_or_almacen_required(view_func):
    """Decorador para admin o almacén"""
    return role_required(['admin', 'almacen'])(view_func)

def vendedor_can_view(view_func):
    """
    Vendedor solo puede ver (GET, HEAD), admin y almacén pueden todo.
    Útil para vistas que necesitan permisos diferenciados por método HTTP.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied('Debes iniciar sesión')
        
        user_role = request.user.profile.role
        
        # Admin y almacén tienen todos los permisos
        if user_role in ['admin', 'almacen']:
            return view_func(request, *args, **kwargs)
        
        # Vendedor solo puede ver (métodos seguros)
        if user_role == 'vendedor' and request.method in ['GET', 'POST','HEAD']:
            return view_func(request, *args, **kwargs)
        
        # Otros casos: denegar permiso
        raise PermissionDenied('No tienes permiso para realizar esta acción')
    return wrapper

# Decorador para mixins de Class-Based Views (útil si prefieres este enfoque)
class RoleRequiredMixin:
    """Mixin para Class-Based Views que requiere ciertos roles"""
    allowed_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied('Debes iniciar sesión')
        
        user_role = request.user.profile.role
        if user_role not in self.allowed_roles:
            raise PermissionDenied('No tienes permiso para acceder a esta sección')
        
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin']

class AlmacenRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['almacen']

class AdminOrAlmacenRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin', 'almacen']