# Manual de Usuario - Administrador
## Sistema Mini ERP

---

## 1. Inicio de Sesión

### Acceder al sistema
1. Abre tu navegador y accede a: `http://localhost:8000/`
2. Introduce tu **nombre de usuario** y **contraseña**
3. Haz clic en **"Entrar"**

### Tras el login
Serás redirigido automáticamente al **Dashboard de Administrador**.

---

## 2. Dashboard de Administrador

El dashboard muestra:
- Tu nombre de usuario y rol (Admin)
- **Estadísticas**:
  - Total de productos
  - Productos con stock bajo
  - Productos sin stock
- **Accesos rápidos**:
  - Panel de Admin Django
  - Gestionar Inventario
- **Información del usuario**

### Navegación (barra superior)
La barra de navegación contiene:
- **ERP Sistema** (logo) - Regresa al dashboard
- **Inventario** - Gestionar productos
- **Admin Panel** - Panel de administración Django
- **Tu usuario** (dropdown) - Menú con:
  - Tu nombre + badge "Admin"
  - "Mi Perfil"
  - "Cerrar Sesión"

---

## 3. Gestionar Productos (Inventario)

### Acceder al inventario
1. Haz clic en **"Inventario"** en el menú superior
2. Verás la lista de todos los productos

### Información mostrada
| Campo | Descripción |
|-------|-------------|
| Código | Identificador único del producto |
| Nombre | Nombre del producto |
| Descripción | Detalles del producto |
| Precio | Precio en soles (S/.) |
| Stock | Cantidad disponible |
| Estado | Disponible / Stock bajo / Sin stock |
| Acciones | Editar / Eliminar |

### Estados de stock
- 🟢 **Verde**: Stock disponible (más de 5 unidades)
- 🟡 **Amarillo**: Stock bajo (5 o menos unidades)
- 🔴 **Rojo**: Sin stock (0 unidades)

---

## 4. Crear Nuevo Producto

### Pasos
1. Desde el inventario, haz clic en **"Nuevo Producto"** (botón azul)
2. O desde el dashboard, haz clic en **"Gestionar Inventario"**
3. Rellena el formulario:
   - **Código**: Identificador único (ej: PROD-001)
   - **Nombre**: Nombre del producto
   - **Descripción**: Detalles adicionales (opcional)
   - **Precio**: Precio en soles (ej: 150.00)
   - **Stock**: Cantidad inicial
4. Haz clic en **"Guardar Producto"**

### Mensaje de éxito
Verás un mensaje verde confirmando la creación.

---

## 5. Editar Producto

### Pasos
1. En la lista de productos, haz clic en el botón de **lápiz** (editar)
2. Modifica los campos necesarios
3. Haz clic en **"Actualizar Producto"**

### Mensaje de éxito
Verás un mensaje verde confirmando la actualización.

---

## 6. Eliminar Producto

### Pasos
1. En la lista de productos, haz clic en el botón de **basura** (eliminar)
2. Aparecerá una ventana de confirmación
3. Haz clic en **"Sí, eliminar"** para confirmar

### ⚠️ Advertencia
La eliminación es permanente y no se puede deshacer.

---

## 7. Gestionar Compras

### Acceder a compras
Desde el menú, busca el enlace a **Compras** (si está disponible) o usa `/compras/`

### Funcionalidades de compras:
- Ver historial de compras
- Registrar nueva compra
- Ver detalle de compra
- Anular compra (revierte el stock)

### Registrar compra
1. Haz clic en **"Nueva Compra"**
2. Completa los datos del proveedor
3. Agrega productos con cantidad y precio
4. El stock se actualiza automáticamente

---

## 8. Panel de Administración Django

### Acceder
Haz clic en **"Admin Panel"** en el menú superior

### Funciones disponibles:
- Gestionar **Usuarios** (crear, editar, eliminar)
- Gestionar **Perfiles** (asignar roles)
- Gestionar **Productos**
- Gestionar **Compras** y detalles
- Ver registros del sistema

### ⚠️ Advertencia
El panel de Django es para administración técnica. Usa el inventario para gestión diaria de productos.

---

## 9. Buscar Productos

Usa la barra de búsqueda para filtrar por:
- Código
- Nombre
- Descripción

---

## 10. Cerrar Sesión

1. Haz clic en tu nombre de usuario (esquina superior derecha)
2. Se abrirá un menú desplegable
3. Haz clic en **"Cerrar Sesión"**

---

## 11. Roles del Sistema

| Rol | Permisos |
|-----|-----------|
| **Admin** | Acceso completo a todo |
| **Almacén** | Gestionar inventario (CRUD productos) |
| **Vendedor** | Solo ver productos |

---

## 12. Solución de Problemas

| Problema | Solución |
|----------|----------|
| No puedo iniciar sesión | Verifica tu usuario y contraseña |
| No puedo crear producto | Revisa que todos los campos requeridos estén llenos |
| Código duplicado | Cada producto debe tener un código único |
| Error en compras | Verifica que los productos existan |
| La página no carga | Refresca el navegador o contacta al admin |

---

## 13. Iconos utilizados

El sistema usa iconos de **Bootstrap Icons**:
- 📦 `Inventario` - Icono de caja
- ➕ `Nuevo` - Icono de suma
- ✏️ `Editar` - Icono de lápiz
- 🗑️ `Eliminar` - Icono de basuración
- 🛒 `Compras` - Icono de carrito
- 🛡️ `Admin Panel` - Icono de escudo
- 👤 `Usuario` - Icono de persona

---

## 14. Contacto

Si tienes problemas técnicos o necesitas ayuda adicional, contacta al administrador del sistema.

---

*Manual generado para el rol de Administrador - Mini ERP*