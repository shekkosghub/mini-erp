from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponse
from .models import Profile, Producto
from .signals import create_user_profile, save_user_profile

# ==================== PRUEBAS DEL MODELO PROFILE ====================

class ProfileModelTest(TestCase):
    """Pruebas para el modelo Profile"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_profile_created_automatically(self):
        """Verificar que se crea un perfil automáticamente al crear usuario"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_str_method(self):
        """Probar el método __str__ del perfil"""
        expected_str = f"{self.user.username} - Vendedor"
        self.assertEqual(str(self.user.profile), expected_str)
    
    def test_profile_default_role(self):
        """Verificar que el rol por defecto es 'vendedor'"""
        self.assertEqual(self.user.profile.role, 'vendedor')
    
    def test_profile_role_choices(self):
        """Probar que se pueden asignar diferentes roles"""
        roles = ['admin', 'vendedor', 'almacen']
        
        for role in roles:
            self.user.profile.role = role
            self.user.profile.save()
            self.user.refresh_from_db()
            self.assertEqual(self.user.profile.role, role)
    
    def test_profile_verbose_names(self):
        """Probar los nombres verbosos del modelo"""
        self.assertEqual(str(Profile._meta.verbose_name), 'Perfil')
        self.assertEqual(str(Profile._meta.verbose_name_plural), 'Perfiles')
    
    def test_one_to_one_relationship(self):
        """Verificar la relación OneToOne entre User y Profile"""
        user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.assertEqual(user2.profile.user, user2)
        
        # Verificar que no se puede crear otro perfil para el mismo usuario
        with self.assertRaises(Exception):
            Profile.objects.create(user=self.user, role='admin')


# ==================== PRUEBAS DEL MODELO PRODUCTO ====================

class ProductoModelTest(TestCase):
    """Pruebas para el modelo Producto"""
    
    def setUp(self):
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Laptop HP',
            descripcion='Laptop de 16GB RAM',
            precio=2500.00,
            stock=10
        )
    
    def test_producto_creation(self):
        """Verificar creación de producto"""
        self.assertEqual(self.producto.codigo, 'PROD-001')
        self.assertEqual(self.producto.nombre, 'Laptop HP')
        self.assertEqual(self.producto.precio, 2500.00)
        self.assertEqual(self.producto.stock, 10)
    
    def test_producto_str_method(self):
        """Probar método __str__ del producto"""
        expected_str = "PROD-001 - Laptop HP"
        self.assertEqual(str(self.producto), expected_str)
    
    def test_producto_unique_codigo(self):
        """Verificar que el código es único"""
        with self.assertRaises(Exception):
            Producto.objects.create(
                codigo='PROD-001',  # Código duplicado
                nombre='Otro Producto',
                precio=100.00,
                stock=5
            )
    
    def test_producto_default_stock(self):
        """Verificar que el stock por defecto es 0"""
        producto_sin_stock = Producto.objects.create(
            codigo='PROD-002',
            nombre='Producto sin stock',
            precio=100.00
        )
        self.assertEqual(producto_sin_stock.stock, 0)
    
    def test_producto_blank_descripcion(self):
        """Verificar que la descripción puede estar en blanco"""
        producto_sin_desc = Producto.objects.create(
            codigo='PROD-003',
            nombre='Sin descripción',
            precio=50.00,
            descripcion=''
        )
        self.assertEqual(producto_sin_desc.descripcion, '')
    
    def test_producto_auto_timestamps(self):
        """Verificar que los timestamps se crean automáticamente"""
        self.assertIsNotNone(self.producto.created_at)
        self.assertIsNotNone(self.producto.updated_at)
    
    def test_producto_verbose_names(self):
        """Probar nombres verbosos del modelo"""
        self.assertEqual(str(Producto._meta.verbose_name), 'Producto')
        self.assertEqual(str(Producto._meta.verbose_name_plural), 'Productos')
    
    def test_producto_ordering(self):
        """Verificar que los productos se ordenan por nombre por defecto"""
        Producto.objects.create(codigo='PROD-004', nombre='Zapatos', precio=100)
        Producto.objects.create(codigo='PROD-005', nombre='Audifonos', precio=50)
        Producto.objects.create(codigo='PROD-006', nombre='Camisa', precio=80)
        
        productos = Producto.objects.all()
        nombres = [p.nombre for p in productos]
        self.assertEqual(nombres, sorted(nombres))
    
    def test_producto_get_absolute_url(self):
        """Probar el método get_absolute_url"""
        url = self.producto.get_absolute_url()
        self.assertEqual(url, reverse('erp:producto_list'))


# ==================== PRUEBAS DE SEÑALES ====================

class SignalsTest(TestCase):
    """Pruebas para las señales post_save"""
    
    def test_create_profile_signal(self):
        """Probar que la señal create_user_profile funciona correctamente"""
        user = User.objects.create_user(username='signaluser', password='testpass')
        self.assertTrue(Profile.objects.filter(user=user).exists())
    
    def test_save_profile_signal(self):
        """Probar que la señal save_user_profile guarda cambios en el perfil"""
        user = User.objects.create_user(username='saveuser', password='testpass')
        user.profile.role = 'admin'
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.profile.role, 'admin')
    
    def test_multiple_users_multiple_profiles(self):
        """Probar creación de múltiples usuarios con sus respectivos perfiles"""
        users_data = [
            ('user1', 'admin'),
            ('user2', 'vendedor'),
            ('user3', 'almacen'),
        ]
        
        created_users = []
        for username, role in users_data:
            user = User.objects.create_user(username=username, password='testpass')
            user.profile.role = role
            user.profile.save()
            created_users.append(user)
        
        for user in created_users:
            profile = Profile.objects.get(user=user)
            self.assertIsNotNone(profile)
            self.assertEqual(profile.user, user)


# ==================== PRUEBAS DE VISTAS DE DASHBOARD ====================

class DashboardViewsTest(TestCase):
    """Pruebas para las vistas de dashboard según rol"""
    
    def setUp(self):
        self.client = Client()
        
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass123'
        )
        self.admin_user.profile.role = 'admin'
        self.admin_user.profile.save()
        
        self.vendedor_user = User.objects.create_user(
            username='vendedoruser',
            password='vendedorpass123'
        )
        self.vendedor_user.profile.role = 'vendedor'
        self.vendedor_user.profile.save()
        
        self.almacen_user = User.objects.create_user(
            username='almacenuser',
            password='almacenpass123'
        )
        self.almacen_user.profile.role = 'almacen'
        self.almacen_user.profile.save()
        
        # Crear productos para pruebas
        Producto.objects.create(codigo='P001', nombre='Producto 1', precio=100, stock=10)
        Producto.objects.create(codigo='P002', nombre='Producto 2', precio=200, stock=2)
        Producto.objects.create(codigo='P003', nombre='Producto 3', precio=300, stock=0)
    
    def test_admin_dashboard_access(self):
        """Verificar acceso al dashboard de admin"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(reverse('erp:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'erp/admin_dashboard.html')
    
    def test_vendedor_dashboard_access(self):
        """Verificar acceso al dashboard de vendedor"""
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(reverse('erp:vendedor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'erp/vendedor_dashboard.html')
    
    def test_almacen_dashboard_access(self):
        """Verificar acceso al dashboard de almacén"""
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(reverse('erp:almacen_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'erp/almacen_dashboard.html')
    
    def test_dashboard_requires_login(self):
        """Verificar que los dashboards requieren autenticación"""
        response = self.client.get(reverse('erp:admin_dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/admin_dashboard/')
    
    def test_admin_dashboard_context(self):
        """Verificar contexto del dashboard de admin"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(reverse('erp:admin_dashboard'))
        
        self.assertEqual(response.context['total_productos'], 3)
        self.assertEqual(response.context['stock_bajo'], 2)  # P002 (stock=2) + P003 (stock=0)
        self.assertEqual(response.context['sin_stock'], 1)   # P003 con stock=0
    
    def test_vendedor_dashboard_context(self):
        """Verificar contexto del dashboard de vendedor"""
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(reverse('erp:vendedor_dashboard'))
        
        self.assertEqual(response.context['total_productos_disponibles'], 2)  # Productos con stock > 0
        self.assertEqual(len(response.context['productos_destacados']), 2)
    
    def test_almacen_dashboard_context(self):
        """Verificar contexto del dashboard de almacén"""
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(reverse('erp:almacen_dashboard'))
        
        self.assertEqual(response.context['total_productos'], 3)
        self.assertEqual(response.context['stock_total'], 12)  # 10 + 2 + 0
        self.assertEqual(len(response.context['productos_bajo_stock']), 2)  # Producto 2 y 3


# ==================== PRUEBAS DE VISTAS DE INVENTARIO ====================

class InventarioViewsTest(TestCase):
    """Pruebas para el CRUD de inventario"""
    
    def setUp(self):
        self.client = Client()
        
        # Crear usuarios con diferentes roles
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass123'
        )
        self.admin_user.profile.role = 'admin'
        self.admin_user.profile.save()
        
        self.vendedor_user = User.objects.create_user(
            username='vendedoruser',
            password='vendedorpass123'
        )
        self.vendedor_user.profile.role = 'vendedor'
        self.vendedor_user.profile.save()
        
        self.almacen_user = User.objects.create_user(
            username='almacenuser',
            password='almacenpass123'
        )
        self.almacen_user.profile.role = 'almacen'
        self.almacen_user.profile.save()
        
        # Crear producto de prueba
        self.producto = Producto.objects.create(
            codigo='TEST-001',
            nombre='Producto Test',
            descripcion='Descripción test',
            precio=100.00,
            stock=5
        )
        
        self.list_url = reverse('erp:producto_list')
        self.create_url = reverse('erp:producto_create')
        self.update_url = reverse('erp:producto_update', args=[self.producto.pk])
        self.delete_url = reverse('erp:producto_delete', args=[self.producto.pk])
    
    # Pruebas de lista de productos
    def test_producto_list_access_for_admin(self):
        """Admin puede ver lista de productos"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventario/producto_list.html')
    
    def test_producto_list_access_for_vendedor(self):
        """Vendedor puede ver lista de productos"""
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventario/producto_list.html')
    
    def test_producto_list_access_for_almacen(self):
        """Almacén puede ver lista de productos"""
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
    
    def test_producto_list_requires_login(self):
        """Lista de productos requiere autenticación"""
        response = self.client.get(self.list_url)
        self.assertRedirects(response, '/accounts/login/?next=/inventario/')
    
    def test_producto_list_search(self):
        """Probar búsqueda de productos"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto Test')
    
    def test_producto_list_pagination(self):
        """Probar paginación en lista de productos"""
        # Crear 15 productos
        for i in range(15):
            Producto.objects.create(
                codigo=f'PAG-{i:03d}',
                nombre=f'Producto {i}',
                precio=100,
                stock=10
            )
        
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['productos']), 10)  # 10 por página
    
    # Pruebas de creación de productos
    def test_producto_create_access_for_admin(self):
        """Admin puede crear productos"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
    
    def test_producto_create_access_for_almacen(self):
        """Almacén puede crear productos"""
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
    
    def test_producto_create_denied_for_vendedor(self):
        """Vendedor NO puede crear productos"""
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 403)
    
    def test_producto_create_success(self):
        """Probar creación exitosa de producto"""
        self.client.login(username='adminuser', password='adminpass123')
        data = {
            'codigo': 'NUEVO-001',
            'nombre': 'Nuevo Producto',
            'descripcion': 'Descripción nueva',
            'precio': 150.00,
            'stock': 20
        }
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Producto.objects.filter(codigo='NUEVO-001').exists())
    
    def test_producto_create_duplicate_codigo(self):
        """Probar creación con código duplicado"""
        self.client.login(username='adminuser', password='adminpass123')
        data = {
            'codigo': 'TEST-001',  # Código ya existente
            'nombre': 'Producto Duplicado',
            'precio': 100.00,
            'stock': 5
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)  # Vuelve al formulario con error
        self.assertFalse(Producto.objects.filter(nombre='Producto Duplicado').exists())
    
    # Pruebas de edición de productos
    def test_producto_update_access_for_admin(self):
        """Admin puede editar productos"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
    
    def test_producto_update_access_for_almacen(self):
        """Almacén puede editar productos"""
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
    
    def test_producto_update_denied_for_vendedor(self):
        """Vendedor NO puede editar productos"""
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 403)
    
    def test_producto_update_success(self):
        """Probar actualización exitosa de producto"""
        self.client.login(username='adminuser', password='adminpass123')
        data = {
            'codigo': 'TEST-001',
            'nombre': 'Producto Actualizado',
            'descripcion': 'Descripción actualizada',
            'precio': 200.00,
            'stock': 15
        }
        response = self.client.post(self.update_url, data)
        self.assertRedirects(response, self.list_url)
        
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Producto Actualizado')
        self.assertEqual(self.producto.precio, 200.00)
        self.assertEqual(self.producto.stock, 15)
    
    # Pruebas de eliminación de productos
    def test_producto_delete_access_for_admin(self):
        """Admin puede eliminar productos"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventario/producto_confirm_delete.html')
    
    def test_producto_delete_access_for_almacen(self):
        """Almacén puede eliminar productos"""
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
    
    def test_producto_delete_denied_for_vendedor(self):
        """Vendedor NO puede eliminar productos"""
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)
    
    def test_producto_delete_success(self):
        """Probar eliminación exitosa de producto"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.post(self.delete_url, {})
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())
    
    def test_producto_delete_nonexistent(self):
        """Probar eliminación de producto inexistente"""
        self.client.login(username='adminuser', password='adminpass123')
        url = reverse('erp:producto_delete', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


# ==================== PRUEBAS DE REDIRECCIÓN HOME ====================

class HomeViewTest(TestCase):
    """Pruebas para la vista home y redirección según rol"""
    
    def setUp(self):
        self.client = Client()
        
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass123'
        )
        self.admin_user.profile.role = 'admin'
        self.admin_user.profile.save()
        
        self.vendedor_user = User.objects.create_user(
            username='vendedoruser',
            password='vendedorpass123'
        )
        self.vendedor_user.profile.role = 'vendedor'
        self.vendedor_user.profile.save()
        
        self.almacen_user = User.objects.create_user(
            username='almacenuser',
            password='almacenpass123'
        )
        self.almacen_user.profile.role = 'almacen'
        self.almacen_user.profile.save()
        
        self.home_url = reverse('erp:home')
    
    def test_home_redirects_admin_to_admin_dashboard(self):
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('erp:admin_dashboard'))
    
    def test_home_redirects_vendedor_to_vendedor_dashboard(self):
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('erp:vendedor_dashboard'))
    
    def test_home_redirects_almacen_to_almacen_dashboard(self):
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('erp:almacen_dashboard'))
    
    def test_home_requires_login(self):
        response = self.client.get(self.home_url)
        self.assertRedirects(response, '/accounts/login/?next=/')
    
    def test_home_with_invalid_role(self):
        invalid_user = User.objects.create_user(
            username='invaliduser',
            password='invalidpass'
        )
        invalid_user.profile.role = 'rol_invalido'
        invalid_user.profile.save()
        
        self.client.login(username='invaliduser', password='invalidpass')
        response = self.client.get(self.home_url, follow=True)
        
        messages = list(response.context['messages'])
        self.assertTrue(any('Rol no válido' in str(message) for message in messages))


# ==================== PRUEBAS DE INTEGRACIÓN ====================

class IntegrationTest(TestCase):
    """Pruebas de integración del sistema completo"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.admin_user.profile.role = 'admin'
        self.admin_user.profile.save()
    
    def test_complete_product_workflow(self):
        """Flujo completo: crear -> listar -> editar -> eliminar"""
        self.client.login(username='admin', password='admin123')
        
        # 1. Crear producto
        create_data = {
            'codigo': 'FLOW-001',
            'nombre': 'Producto Flujo',
            'descripcion': 'Prueba completa',
            'precio': 99.99,
            'stock': 10
        }
        response = self.client.post(reverse('erp:producto_create'), create_data)
        self.assertRedirects(response, reverse('erp:producto_list'))
        
        producto = Producto.objects.get(codigo='FLOW-001')
        self.assertEqual(producto.nombre, 'Producto Flujo')
        
        # 2. Listar productos (debe aparecer)
        response = self.client.get(reverse('erp:producto_list'))
        self.assertContains(response, 'Producto Flujo')
        
        # 3. Editar producto
        update_data = {
            'codigo': 'FLOW-001',
            'nombre': 'Producto Modificado',
            'descripcion': 'Descripción modificada',
            'precio': 149.99,
            'stock': 25
        }
        response = self.client.post(reverse('erp:producto_update', args=[producto.pk]), update_data)
        self.assertRedirects(response, reverse('erp:producto_list'))
        
        producto.refresh_from_db()
        self.assertEqual(producto.nombre, 'Producto Modificado')
        self.assertEqual(float(producto.precio), 149.99)
        
        # 4. Eliminar producto
        response = self.client.post(reverse('erp:producto_delete', args=[producto.pk]), {})
        self.assertRedirects(response, reverse('erp:producto_list'))
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())
    
    def test_access_control_workflow(self):
        """Verificar control de acceso según rol"""
        # Admin puede crear
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('erp:producto_create'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        
        # Vendedor no puede crear
        vendedor = User.objects.create_user(username='vendedor', password='vendedor123')
        vendedor.profile.role = 'vendedor'
        vendedor.profile.save()
        
        self.client.login(username='vendedor', password='vendedor123')
        response = self.client.get(reverse('erp:producto_create'))
        self.assertEqual(response.status_code, 403)
        self.client.logout()


# ==================== PRUEBAS DE DECORADORES ====================

class DecoratorsTest(TestCase):
    """Pruebas para los decoradores de roles"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='admin123')
        self.admin_user.profile.role = 'admin'
        self.admin_user.profile.save()
        
        self.vendedor_user = User.objects.create_user(username='vendedor', password='vendedor123')
        self.vendedor_user.profile.role = 'vendedor'
        self.vendedor_user.profile.save()
    
    def test_admin_or_almacen_decorator_allows_admin(self):
        """Decorador permite acceso a admin"""
        from .decorators import admin_or_almacen_required
        
        @admin_or_almacen_required
        def test_view(request):
            return HttpResponse("OK")
        
        # Simular request con admin
        request = self.client.request().wsgi_request
        request.user = self.admin_user
        
        response = test_view(request)
        self.assertEqual(response.content, b"OK")
    
    def test_admin_or_almacen_decorator_denies_vendedor(self):
        """Decorador deniega acceso a vendedor"""
        from .decorators import admin_or_almacen_required
        
        @admin_or_almacen_required
        def test_view(request):
            return HttpResponse("OK")
        
        request = self.client.request().wsgi_request
        request.user = self.vendedor_user
        
        with self.assertRaises(PermissionDenied):
            test_view(request)


# ==================== PRUEBAS DE CASOS EXTREMO ====================

class EdgeCasesTest(TestCase):
    """Pruebas para casos extremos"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.user.profile.role = 'admin'
        self.user.profile.save()
        self.client.login(username='testuser', password='test123')
    
    def test_create_product_with_max_stock(self):
        """Crear producto con stock máximo"""
        producto = Producto.objects.create(
            codigo='MAX-001',
            nombre='Stock Máximo',
            precio=100,
            stock=999999
        )
        self.assertEqual(producto.stock, 999999)
    
    def test_create_product_with_zero_price(self):
        """Crear producto con precio cero"""
        producto = Producto.objects.create(
            codigo='ZERO-001',
            nombre='Precio Cero',
            precio=0,
            stock=10
        )
        self.assertEqual(producto.precio, 0)
    
    def test_create_product_with_negative_stock(self):
        """Crear producto con stock negativo (debería permitirse?)"""
        producto = Producto.objects.create(
            codigo='NEG-001',
            nombre='Stock Negativo',
            precio=100,
            stock=-5
        )
        self.assertEqual(producto.stock, -5)
    
    def test_search_product_with_special_characters(self):
        """Buscar productos con caracteres especiales"""
        Producto.objects.create(
            codigo='SPECIAL',
            nombre='Producto Especial!@#$%',
            precio=100,
            stock=10
        )
        
        response = self.client.get(reverse('erp:producto_list'), {'search': '!@#$%'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Producto Especial')
    
    def test_long_product_name(self):
        """Crear producto con nombre muy largo"""
        nombre_largo = 'A' * 200
        producto = Producto.objects.create(
            codigo='LONG-001',
            nombre=nombre_largo,
            precio=100,
            stock=10
        )
        self.assertEqual(len(producto.nombre), 200)
    
    def test_update_nonexistent_product(self):
        """Intentar actualizar producto inexistente"""
        url = reverse('erp:producto_update', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_access_product_list_without_products(self):
        """Lista de productos vacía"""
        Producto.objects.all().delete()
        response = self.client.get(reverse('erp:producto_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay productos registrados')


# ==================== PRUEBAS DE URLS ====================

class URLConfigurationTest(TestCase):
    """Pruebas para la configuración de URLs"""
    
    def test_home_url_resolves(self):
        from django.urls import resolve
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'erp:home')
    
    def test_login_url_resolves(self):
        from django.urls import resolve
        resolver = resolve('/accounts/login/')
        self.assertEqual(resolver.view_name, 'login')
    
    def test_producto_list_url_resolves(self):
        from django.urls import resolve
        resolver = resolve('/inventario/')
        self.assertEqual(resolver.view_name, 'erp:producto_list')
    
    def test_producto_create_url_resolves(self):
        from django.urls import resolve
        resolver = resolve('/inventario/crear/')
        self.assertEqual(resolver.view_name, 'erp:producto_create')
    
    def test_producto_update_url_resolves(self):
        from django.urls import resolve
        resolver = resolve('/inventario/editar/1/')
        self.assertEqual(resolver.view_name, 'erp:producto_update')
    
    def test_producto_delete_url_resolves(self):
        from django.urls import resolve
        resolver = resolve('/inventario/eliminar/1/')
        self.assertEqual(resolver.view_name, 'erp:producto_delete')