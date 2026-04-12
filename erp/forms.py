from django import forms
from django.forms import inlineformset_factory
from .models import Compra, DetalleCompra, Producto

class CompraForm(forms.ModelForm):
    """Formulario para la compra"""
    class Meta:
        model = Compra
        fields = ['proveedor', 'observaciones']
        widgets = {
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proveedor'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales...'
            }),
        }

class DetalleCompraForm(forms.ModelForm):
    """Formulario para detalles de compra"""
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control cantidad-input',
                'min': 1,
                'value': 1
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control precio-input',
                'step': '0.01',
                'min': 0
            }),
        }

# Crear el formset para detalles de compra (versión corregida)
DetalleCompraFormSet = inlineformset_factory(
    Compra,
    DetalleCompra,
    form=DetalleCompraForm,
    extra=0,  # Número de formularios vacíos
    can_delete=True,
    min_num=1,  # Mínimo 1 detalle
    validate_min=True,
    # verify_exists fue eliminado en Django 1.10+
)

from .models import Cliente, Venta, DetalleVenta

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_venta']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'min': 1, 'value': 1}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control precio-input', 'step': '0.01', 'min': 0}),
        }
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0')
        return cantidad
    
    def clean_precio_venta(self):
        precio = self.cleaned_data.get('precio_venta')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio

# Formset dinámico (sin mínimo, con extra=0, manejaremos filas con JS)
DetalleVentaFormSet = inlineformset_factory(
    Venta,
    DetalleVenta,
    form=DetalleVentaForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=False,
)