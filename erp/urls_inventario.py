from django.urls import path
from .views import inventario

app_name = 'inventario'

urlpatterns = [
    path('', inventario.ProductoListView.as_view(), name='producto_list'),
    path('crear/', inventario.ProductoCreateView.as_view(), name='producto_create'),
    path('editar/<int:pk>/', inventario.ProductoUpdateView.as_view(), name='producto_update'),
    path('eliminar/<int:pk>/', inventario.ProductoDeleteView.as_view(), name='producto_delete'),
]