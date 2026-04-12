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
    # URLs de compras
    path('compras/', views.CompraListView.as_view(), name='compra_list'),
    path('compras/<int:pk>/', views.CompraDetailView.as_view(), name='compra_detail'),
    path('compras/crear/', views.CompraCreateView.as_view(), name='compra_create'),
    path('compras/eliminar/<int:pk>/', views.CompraDeleteView.as_view(), name='compra_delete'),
    path('compras/anular/<int:pk>/', views.CompraAnularView.as_view(), name='compra_anular'),
    # Ventas
    path('ventas/', views.VentaListView.as_view(), name='venta_list'),
    path('ventas/<int:pk>/', views.VentaDetailView.as_view(), name='venta_detail'),
    path('ventas/crear/', views.VentaCreateView.as_view(), name='venta_create'),

]