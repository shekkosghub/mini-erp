from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import Compra, DetalleCompra, Producto
from ..forms import CompraForm, DetalleCompraFormSet
from ..services import CompraService
from ..decorators import admin_or_almacen_required
from django.utils.decorators import method_decorator

@method_decorator(admin_or_almacen_required, name='dispatch')
class CompraListView(LoginRequiredMixin, ListView):
    """Lista de compras"""
    model = Compra
    template_name = 'compras/compra_list.html'
    context_object_name = 'compras'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        proveedor = self.request.GET.get('proveedor', '')
        
        if proveedor:
            queryset = queryset.filter(proveedor__icontains=proveedor)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedor_filter'] = self.request.GET.get('proveedor', '')
        context['user_role'] = self.request.user.profile.role
        return context

@method_decorator(admin_or_almacen_required, name='dispatch')
class CompraDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una compra"""
    model = Compra
    template_name = 'compras/compra_detail.html'
    context_object_name = 'compra'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.object.get_total()
        return context

@method_decorator(admin_or_almacen_required, name='dispatch')
class CompraCreateView(LoginRequiredMixin, CreateView):
    """
    Crear una nueva compra con formset de detalles.
    Al guardar, actualiza automáticamente el stock de productos.
    """
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compra_form.html'
    
    def get_context_data(self, **kwargs):
        """Añade el formset al contexto"""
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['formset'] = DetalleCompraFormSet(self.request.POST)
        else:
            context['formset'] = DetalleCompraFormSet()
        
        # Añadir productos para el JSON (para autocompletado)
        context['productos'] = Producto.objects.all()
        
        return context
    
    def form_valid(self, form):
        """Procesa el formulario principal y el formset"""
        context = self.get_context_data()
        formset = context['formset']
        
        # Validar formset
        if not formset.is_valid():
            messages.error(self.request, 'Error en los detalles de la compra. Por favor corrige los errores.')
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        
        # Verificar que haya al menos un detalle
        if len(formset.cleaned_data) == 0 or all(d.get('DELETE', False) for d in formset.cleaned_data):
            messages.error(self.request, 'Debes agregar al menos un producto a la compra.')
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        
        try:
            # Usar transacción atómica para garantizar integridad
            with transaction.atomic():
                # Guardar la compra
                compra = form.save()
                
                # Preparar datos de detalles
                detalles_data = []
                for detalle_form in formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        detalles_data.append({
                            'producto': detalle_form.cleaned_data['producto'],
                            'cantidad': detalle_form.cleaned_data['cantidad'],
                            'precio_unitario': detalle_form.cleaned_data['precio_unitario'],
                        })
                
                # Procesar la compra (crea detalles y actualiza stock)
                CompraService.procesar_compra(compra, detalles_data)
                
                messages.success(
                    self.request, 
                    f'¡Compra a {compra.proveedor} registrada exitosamente! '
                    f'Se actualizó el stock de {len(detalles_data)} productos.'
                )
                
                return redirect('erp:compra_detail', pk=compra.pk)
                
        except Exception as e:
            messages.error(self.request, f'Error al procesar la compra: {str(e)}')
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
    
    def form_invalid(self, form):
        """Si el formulario principal es inválido"""
        messages.error(self.request, 'Error en el formulario. Por favor corrige los errores.')
        return self.render_to_response(self.get_context_data(form=form))

@method_decorator(admin_or_almacen_required, name='dispatch')
class CompraDeleteView(LoginRequiredMixin, DeleteView):
    """
    Eliminar una compra (solo si es necesario).
    NOTA: No actualiza el stock automáticamente para evitar pérdida de datos.
    Para revertir una compra, usa la vista de anulación.
    """
    model = Compra
    template_name = 'compras/compra_confirm_delete.html'
    success_url = reverse_lazy('erp:compra_list')
    
    def delete(self, request, *args, **kwargs):
        compra = self.get_object()
        proveedor = compra.proveedor
        
        # Verificar si la compra tiene detalles
        if compra.detalles.exists():
            messages.warning(
                request, 
                f'No se puede eliminar la compra a {proveedor} porque ya afectó el inventario. '
                f'Usa la opción de anulación si es necesario.'
            )
            return redirect('erp:compra_detail', pk=compra.pk)
        
        messages.success(request, f'Compra a {proveedor} eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

@method_decorator(admin_or_almacen_required, name='dispatch')
class CompraAnularView(LoginRequiredMixin, DetailView):
    """Vista para anular una compra y revertir el stock"""
    model = Compra
    template_name = 'compras/compra_anular.html'
    context_object_name = 'compra'
    
    def post(self, request, *args, **kwargs):
        compra = self.get_object()
        
        try:
            # Anular la compra (resta el stock)
            CompraService.anular_compra(compra)
            
            messages.success(
                request,
                f'Compra a {compra.proveedor} anulada exitosamente. '
                f'El stock ha sido revertido.'
            )
            
            return redirect('erp:compra_list')
            
        except Exception as e:
            messages.error(request, f'Error al anular la compra: {str(e)}')
            return redirect('erp:compra_detail', pk=compra.pk)