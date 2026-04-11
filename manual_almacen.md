# Manual de Usuario - Almacén
## Sistema Mini ERP

---

## 1. Inicio de Sesión

### Acceder al sistema
1. Abre tu navegador y accede a: `http://localhost:8000/`
2. Introduce tu **nombre de usuario** y **contraseña**
3. Haz clic en **"Entrar"**

### Tras el login
Serás redirigido automáticamente al **Dashboard de Almacén**.

---

## 2. Dashboard de Almacén

El dashboard muestra:
- Tu nombre de usuario y rol
- Total de productos en el sistema
- Stock total (suma de todas las unidades)
- Lista de productos con stock bajo (5 o menos unidades)

### Navegación
En la barra superior encontrarás:
- **Inventario** - Gestionar productos
- **Tu nombre** - Menú de usuario con opción de cerrar sesión

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
1. En la página de inventario, haz clic en **"Nuevo Producto"** (botón azul)
2. Rellena el formulario:
   - **Código**: Identificador único (ej: PROD-001)
   - **Nombre**: Nombre del producto
   - **Descripción**: Detalles adicionales (opcional)
   - **Precio**: Precio en soles (ej: 150.00)
   - **Stock**: Cantidad inicial
3. Haz clic en **"Guardar Producto"**

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

### Mensaje de éxito
Verás un mensaje verde confirmando la eliminación.

---

## 7. Buscar Productos

Usa la barra de búsqueda para filtrar por:
- Código
- Nombre
- Descripción

Escribe y presiona **"Buscar"** para filtrar los resultados.

---

## 8. Limitaciones como Almacén

Como almacenista **no puedes**:
- ❌ Acceder al panel de administración
- ❌ Gestionar usuarios
- ❌ Ver estadísticas globales del sistema

---

## 9. Cerrar Sesión

1. Haz clic en tu nombre de usuario (esquina superior derecha)
2. Selecciona **"Cerrar Sesión"**

---

## 10. Solución de Problemas

| Problema | Solución |
|----------|----------|
| No puedo iniciar sesión | Verifica tu usuario y contraseña |
| No puedo crear producto | Revisa que todos los campos requeridos estén llenos |
| Código duplicado | Cada producto debe tener un código único |
| No puedo eliminar | Verifica que el producto existe |
| La página no carga | Refresca el navegador o reinicia el servidor |

---

## 11. Atajos de Teclado

| Acción | Atajo |
|--------|-------|
| Buscar | Enter en campo de búsqueda |
| Guardar | Ctrl + Enter (en formularios) |

---

## 12. Contacto

Si tienes problemas técnicos o necesitas ayuda adicional, contacta al administrador del sistema.

---

*Manual generado para el rol de Almacén - Mini ERP*