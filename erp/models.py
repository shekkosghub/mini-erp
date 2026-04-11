from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Profile(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('vendedor', 'Vendedor'),
        ('almacen', 'Almacen'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLES, default='vendedor')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

class Producto(models.Model):
    codigo = models.CharField('Código', max_length=50, unique=True, help_text='Código único del producto')
    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', blank=True, help_text='Descripción detallada del producto')
    precio = models.DecimalField('Precio', max_digits=10, decimal_places=2, help_text='Precio en soles')
    stock = models.IntegerField('Stock', default=0, help_text='Cantidad disponible')
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['nombre']),
        ]
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def get_absolute_url(self):
        return reverse('erp:producto_list')
class Compra(models.Model):
    """Modelo de compras a proveedores"""
    proveedor = models.CharField('Proveedor', max_length=200, help_text='Nombre del proveedor')
    fecha = models.DateTimeField('Fecha de compra', auto_now_add=True)
    observaciones = models.TextField('Observaciones', blank=True, help_text='Notas adicionales')
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Compra a {self.proveedor} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    def get_total(self):
        """Calcula el total de la compra"""
        return sum(detalle.get_subtotal() for detalle in self.detalles.all())
    
    def get_absolute_url(self):
        return reverse('erp:compra_detail', args=[self.pk])

class DetalleCompra(models.Model):
    """Detalle de compra - productos adquiridos"""
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles', verbose_name='Compra')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='compras', verbose_name='Producto')
    cantidad = models.PositiveIntegerField('Cantidad', help_text='Cantidad comprada')
    precio_unitario = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, help_text='Precio pagado por unidad')
    
    class Meta:
        verbose_name = 'Detalle de compra'
        verbose_name_plural = 'Detalles de compra'
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - {self.compra}"
    
    def get_subtotal(self):
        """Calcula el subtotal del detalle"""
        return self.cantidad * self.precio_unitario    