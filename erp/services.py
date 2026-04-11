from django.db import transaction
from django.db.models import F
from .models import Producto, DetalleCompra

class CompraService:
    """Servicio para manejar la lógica de compras"""
    
    @staticmethod
    @transaction.atomic
    def procesar_compra(compra, detalles_data):
        """
        Procesa una compra: crea los detalles y actualiza el stock de productos.
        Usa transacción atómica para garantizar integridad de datos.
        
        Args:
            compra: Instancia de Compra
            detalles_data: Lista de diccionarios con datos de detalles
        
        Returns:
            compra: Instancia de Compra con detalles creados
        """
        detalles_creados = []
        
        for detalle_data in detalles_data:
            # Obtener el producto
            producto = detalle_data['producto']
            cantidad = detalle_data['cantidad']
            precio_unitario = detalle_data['precio_unitario']
            
            # Crear el detalle de compra
            detalle = DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            detalles_creados.append(detalle)
            
            # Actualizar el stock del producto
            # Usamos F() para evitar condiciones de carrera
            producto.stock = F('stock') + cantidad
            producto.save(update_fields=['stock'])
        
        # Refrescar productos para obtener valores actualizados
        for detalle in detalles_creados:
            detalle.producto.refresh_from_db()
        
        return compra
    
    @staticmethod
    @transaction.atomic
    def anular_compra(compra):
        """
        Anula una compra: resta el stock y elimina los detalles.
        Útil para revertir compras erróneas.
        
        Args:
            compra: Instancia de Compra a anular
        """
        # Restar el stock por cada detalle
        for detalle in compra.detalles.all():
            producto = detalle.producto
            producto.stock = F('stock') - detalle.cantidad
            producto.save(update_fields=['stock'])
            producto.refresh_from_db()
        
        # Eliminar los detalles
        compra.detalles.all().delete()
        
        # Opcional: marcar la compra como anulada en lugar de eliminarla
        # compra.anulada = True
        # compra.save()
        
        return True