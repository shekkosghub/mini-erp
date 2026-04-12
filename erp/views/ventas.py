# erp/views/ventas.py
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import Venta, Producto, Cliente
from ..forms import VentaForm, DetalleVentaFormSet
from ..services import VentaService
from ..decorators import admin_or_almacen_required, vendedor_can_view
from django.utils.decorators import method_decorator

# Solo Admin, Almacén y Vendedor pueden gestionar ventas
@method_decorator(vendedor_can_view, name='dispatch')
class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        cliente = self.request.GET.get('cliente', '')
        if cliente:
            queryset = queryset.filter(cliente__nombre__icontains=cliente)
        return queryset

@method_decorator(vendedor_can_view, name='dispatch')
class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'
    context_object_name = 'venta'

@method_decorator(vendedor_can_view, name='dispatch')
class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/venta_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DetalleVentaFormSet(self.request.POST)
        else:
            context['formset'] = DetalleVentaFormSet()
        context['productos'] = Producto.objects.filter(stock__gt=0)  # solo productos con stock
        context['clientes'] = Cliente.objects.all()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if not formset.is_valid():
            messages.error(self.request, 'Error en los detalles de la venta. Corrige los errores.')
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        
        # Extraer detalles no vacíos y no marcados para eliminar
        detalles_data = []
        for detalle_form in formset:
            if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                producto = detalle_form.cleaned_data.get('producto')
                cantidad = detalle_form.cleaned_data.get('cantidad')
                precio = detalle_form.cleaned_data.get('precio_venta')
                if producto and cantidad and precio:
                    detalles_data.append({
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio_venta': precio,
                    })
        
        if len(detalles_data) == 0:
            messages.error(self.request, 'Debes agregar al menos un producto a la venta.')
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        
        try:
            with transaction.atomic():
                venta = form.save(commit=False)
                venta.total = 0  # temporal
                venta.save()
                VentaService.procesar_venta(venta, detalles_data)
                
            messages.success(self.request, f'Venta #{venta.id} registrada exitosamente. Total: S/ {venta.total:.2f}')
            return redirect('erp:venta_detail', pk=venta.pk)
        
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        except Exception as e:
            messages.error(self.request, f'Error al procesar la venta: {str(e)}')
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario principal.')
        return self.render_to_response(self.get_context_data(form=form))