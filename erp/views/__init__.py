# erp/views/__init__.py
from .home import home, admin_dashboard, vendedor_dashboard, almacen_dashboard
from .inventario import (
    ProductoListView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView
)

__all__ = [
    'home',
    'admin_dashboard',
    'vendedor_dashboard', 
    'almacen_dashboard',
    'ProductoListView',
    'ProductoCreateView',
    'ProductoUpdateView',
    'ProductoDeleteView',
]