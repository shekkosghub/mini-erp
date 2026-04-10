from django.urls import path
from . import views

app_name = 'erp'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('vendedor_dashboard/', views.vendedor_dashboard, name='vendedor_dashboard'),
    path('almacen_dashboard/', views.almacen_dashboard, name='almacen_dashboard'),
]