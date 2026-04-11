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