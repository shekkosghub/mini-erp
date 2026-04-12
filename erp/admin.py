from django.contrib import admin
from .models import Profile, Cliente, Venta, DetalleVenta

admin.site.register(Profile)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono']
    search_fields = ['nombre']