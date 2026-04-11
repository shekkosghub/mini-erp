from django.urls import path, include
from . import views

app_name = 'erp'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('vendedor_dashboard/', views.vendedor_dashboard, name='vendedor_dashboard'),
    path('almacen_dashboard/', views.almacen_dashboard, name='almacen_dashboard'),
    # URLs de inventario
    path('inventario/', views.ProductoListView.as_view(), name='producto_list'),
    path('inventario/crear/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('inventario/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('inventario/eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='producto_delete'),
]