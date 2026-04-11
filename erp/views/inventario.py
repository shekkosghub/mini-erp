# erp/views/inventario.py (corregido)
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from ..models import Producto
from ..decorators import admin_or_almacen_required
from django.utils.decorators import method_decorator

class ProductoListView(LoginRequiredMixin, ListView):
    """
    Lista de productos - Accesible para todos los roles autenticados
    """
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['user_role'] = self.request.user.profile.role
        return context

@method_decorator(admin_or_almacen_required, name='dispatch')
class ProductoCreateView(LoginRequiredMixin, CreateView):
    """
    Crear nuevo producto - Solo Admin y Almacén
    """
    model = Producto
    template_name = 'inventario/producto_form.html'
    fields = ['codigo', 'nombre', 'descripcion', 'precio', 'stock']
    success_url = reverse_lazy('erp:producto_list')  # Cambiado de 'inventario' a 'erp'
    
    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.nombre}" creado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el producto. Por favor corrige los errores.')
        return super().form_invalid(form)

@method_decorator(admin_or_almacen_required, name='dispatch')
class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Editar producto - Solo Admin y Almacén
    """
    model = Producto
    template_name = 'inventario/producto_form.html'
    fields = ['codigo', 'nombre', 'descripcion', 'precio', 'stock']
    success_url = reverse_lazy('erp:producto_list')  # Cambiado de 'inventario' a 'erp'
    
    def form_valid(self, form):
        messages.success(self.request, f'Producto "{form.instance.nombre}" actualizado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el producto. Por favor corrige los errores.')
        return super().form_invalid(form)

@method_decorator(admin_or_almacen_required, name='dispatch')
class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Eliminar producto - Solo Admin y Almacén
    """
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('erp:producto_list')  # Cambiado de 'inventario' a 'erp'
    
    def delete(self, request, *args, **kwargs):
        producto = self.get_object()
        messages.success(request, f'Producto "{producto.nombre}" eliminado exitosamente')
        return super().delete(request, *args, **kwargs)