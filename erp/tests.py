from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .models import Profile
from .signals import create_user_profile, save_user_profile

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
        user.save()  # Esto debería disparar save_user_profile
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
        
        # Verificar que todos los perfiles se crearon correctamente
        for user in created_users:
            profile = Profile.objects.get(user=user)
            self.assertIsNotNone(profile)
            self.assertEqual(profile.user, user)


class HomeViewTest(TestCase):
    """Pruebas para la vista home y redirección según rol"""
    
    def setUp(self):
        """Configuración inicial para pruebas de vistas"""
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
        
        self.home_url = reverse('erp:home')
    
    def test_home_redirects_admin_to_admin_dashboard(self):
        """Verificar que admin es redirigido al dashboard de admin"""
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(self.home_url)
        self.assertRedirects(response, '/admin_dashboard/')  # Ajusta según tu URL
    
    def test_home_redirects_vendedor_to_vendedor_dashboard(self):
        """Verificar que vendedor es redirigido al dashboard de vendedor"""
        self.client.login(username='vendedoruser', password='vendedorpass123')
        response = self.client.get(self.home_url)
        self.assertRedirects(response, '/vendedor_dashboard/')  # Ajusta según tu URL
    
    def test_home_redirects_almacen_to_almacen_dashboard(self):
        """Verificar que almacén es redirigido al dashboard de almacén"""
        self.client.login(username='almacenuser', password='almacenpass123')
        response = self.client.get(self.home_url)
        self.assertRedirects(response, '/almacen_dashboard/')  # Ajusta según tu URL
    
    def test_home_requires_login(self):
        """Verificar que la vista home requiere autenticación"""
        response = self.client.get(self.home_url)
        expected_redirect = '/accounts/login/?next=/'
        self.assertRedirects(response, expected_redirect)
    
    def test_home_with_invalid_role(self):
        """Probar comportamiento con rol inválido"""
        # Crear usuario con rol inválido
        invalid_user = User.objects.create_user(
            username='invaliduser',
            password='invalidpass'
        )
        invalid_user.profile.role = 'rol_invalido'
        invalid_user.profile.save()
        
        self.client.login(username='invaliduser', password='invalidpass')
        response = self.client.get(self.home_url, follow=True)
        
        # Verificar que muestra mensaje de error
        messages = list(response.context['messages'])
        self.assertTrue(any('Rol no válido' in str(message) for message in messages))
    
    def test_profile_accessible_in_view(self):
        """Verificar que el perfil es accesible desde la request en la vista"""
        self.client.login(username='adminuser', password='adminpass123')
        
        # Simular la vista home manualmente para verificar acceso al perfil
        response = self.client.get(self.home_url)
        # El perfil debería ser accesible en la redirección
        self.assertEqual(response.status_code, 302)  # Redirección exitosa


class AuthenticationIntegrationTest(TestCase):
    """Pruebas de integración del sistema de autenticación y roles"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='integuser',
            password='integpass123'
        )
    
    def test_login_and_role_access(self):
        """Probar flujo completo: login, acceso a home, redirección según rol"""
        # Login
        login_success = self.client.login(username='integuser', password='integpass123')
        self.assertTrue(login_success)
        
        # Acceder a home
        response = self.client.get(reverse('erp:home'))
        
        # Verificar redirección según rol (por defecto vendedor)
        self.assertEqual(response.status_code, 302)
    
    def test_role_change_affects_redirection(self):
        """Probar que cambiar el rol afecta la redirección"""
        self.client.login(username='integuser', password='integpass123')
        
        # Probar con rol vendedor
        self.user.profile.role = 'vendedor'
        self.user.profile.save()
        response = self.client.get(reverse('erp:home'))
        self.assertRedirects(response, '/vendedor_dashboard/')
        
        # Cambiar a admin y probar
        self.user.profile.role = 'admin'
        self.user.profile.save()
        response = self.client.get(reverse('erp:home'))
        self.assertRedirects(response, '/admin_dashboard/')
        
        # Cambiar a almacén y probar
        self.user.profile.role = 'almacen'
        self.user.profile.save()
        response = self.client.get(reverse('erp:home'))
        self.assertRedirects(response, '/almacen_dashboard/')
    
    def test_logout_redirect(self):
        """Probar redirección después de logout"""
        self.client.login(username='integuser', password='integpass123')
        response = self.client.get(reverse('erp:home'))
        self.assertEqual(response.status_code, 302)
        
        # Logout
        self.client.logout()
        response = self.client.get(reverse('erp:home'))
        self.assertRedirects(response, '/accounts/login/?next=/')


class ProfileAdminTest(TestCase):
    """Pruebas para el perfil en el panel de administración"""
    
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.client.login(username='admin', password='adminpass123')
    
    def test_profile_registered_in_admin(self):
        """Verificar que Profile está registrado en el admin"""
        from django.contrib.admin.sites import site
        
        # Verificar que el modelo está registrado
        self.assertIn(Profile, site._registry)
    
    def test_can_access_profile_in_admin(self):
        """Verificar que se puede acceder a Profile en el admin"""
        response = self.client.get('/admin/erp/profile/')
        self.assertEqual(response.status_code, 200)
    
    def test_profile_display_in_user_admin(self):
        """Verificar que el perfil se muestra en la página de usuario del admin"""
        response = self.client.get('/admin/auth/user/')
        self.assertEqual(response.status_code, 200)


class EdgeCasesTest(TestCase):
    """Pruebas para casos extremos"""
    
    def test_create_user_without_email(self):
        """Crear usuario sin email debería funcionar"""
        user = User.objects.create_user(username='noemail', password='pass123')
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.email, '')
    
    def test_create_multiple_users_rapidly(self):
        """Crear múltiples usuarios rápidamente no debería causar problemas"""
        for i in range(10):
            user = User.objects.create_user(
                username=f'rapiduser{i}',
                password='pass123'
            )
            self.assertIsNotNone(user.profile)
    
    def test_save_user_without_changing_profile(self):
        """Guardar usuario sin cambiar perfil no debería modificar el rol"""
        user = User.objects.create_user(username='saveuser', password='pass123')
        original_role = user.profile.role
        user.save()  # Guardar sin cambios
        user.refresh_from_db()
        self.assertEqual(user.profile.role, original_role)
    
    def test_delete_user_cascades_to_profile(self):
        """Eliminar usuario debería eliminar su perfil"""
        user = User.objects.create_user(username='todelete', password='pass123')
        profile_id = user.profile.id
        
        user.delete()
        
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=profile_id)


class URLConfigurationTest(TestCase):
    """Pruebas para la configuración de URLs"""
    
    def test_home_url_resolves(self):
        """Verificar que la URL home se resuelve correctamente"""
        from django.urls import resolve
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'erp:home')
    
    def test_login_url_resolves(self):
        """Verificar que la URL de login se resuelve correctamente"""
        from django.urls import resolve
        resolver = resolve('/accounts/login/')
        self.assertEqual(resolver.view_name, 'login')
    
    def test_erp_urls_include_in_core(self):
        """Verificar que las URLs de ERP están incluidas en core"""
        # Esto requiere que ejecutes las pruebas desde el proyecto completo
        response = self.client.get('/')
        # Si no hay autenticación, debería redirigir a login
        self.assertEqual(response.status_code, 302)