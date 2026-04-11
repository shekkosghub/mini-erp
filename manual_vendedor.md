# Manual de Usuario - Vendedor
## Sistema Mini ERP

---

## 1. Inicio de Sesión

### Acceder al sistema
1. Abre tu navegador y accede a: `http://localhost:8000/`
2. Introduce tu **nombre de usuario** y **contraseña**
3. Haz clic en **"Entrar"**

### Tras el login
Serás redirigido automáticamente al **Dashboard de Vendedor** donde podrás ver los productos disponibles.

---

## 2. Dashboard de Vendedor

El dashboard muestra:
- Tu nombre de usuario y rol
- Lista de productos destacados (con stock disponible)
- Total de productos disponibles

### Navegación
En la barra superior encontrarás:
- **Inventario** - Ver lista de productos
- **Tu nombre** - Menú de usuario con opción de cerrar sesión

---

## 3. Ver Productos (Inventario)

### Acceder al inventario
1. Haz clic en **"Inventario"** en el menú superior
2. Verás una tabla con todos los productos disponibles

### Información mostrada
| Campo | Descripción |
|-------|-------------|
| Código | Identificador único del producto |
| Nombre | Nombre del producto |
| Descripción | Detalles del producto |
| Precio | Precio en soles (S/.) |
| Stock | Cantidad disponible |
| Estado | Disponible / Stock bajo / Sin stock |

### Buscar productos
Usa la barra de búsqueda para filtrar por:
- Código
- Nombre
- Descripción

### Estados de stock
- 🟢 **Verde**: Stock disponible (más de 5 unidades)
- 🟡 **Amarillo**: Stock bajo (5 o menos unidades)
- 🔴 **Rojo**: Sin stock (0 unidades)

---

## 4. Limitaciones como Vendedor

Como vendedor **no puedes**:
- ❌ Crear nuevos productos
- ❌ Editar productos existentes
- ❌ Eliminar productos
- ❌ Acceder al panel de administración

Si intentas acceder a estas funciones, recibirás un mensaje de **"Acceso denegado"**.

---

## 5. Cerrar Sesión

1. Haz clic en tu nombre de usuario (esquina superior derecha)
2. Selecciona **"Cerrar Sesión"**

---

## 6. Solución de Problemas

| Problema | Solución |
|----------|----------|
| No puedo iniciar sesión | Verifica tu usuario y contraseña |
| No veo el inventario | Asegúrate de estar logueado |
| No puedo crear productos | Es normal, los vendedores no tienen ese permiso |
| La página no carga | Refresca el navegador o reinicia el servidor |

---

## 7. Contacto

Si tienes problemas técnicos, contacta al administrador del sistema.

---

*Manual generado para el rol de Vendedor - Mini ERP*