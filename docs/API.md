# 📚 Documentación de la API

## Información General

- **Base URL**: `http://localhost:8000`
- **Versión**: 1.0.0
- **Formato de Respuesta**: JSON
- **Autenticación**: JWT Bearer Token

## Autenticación

### Registro de Usuario

**Endpoint**: `POST /auth/register`

**Descripción**: Registra un nuevo usuario en el sistema.

**Cuerpo de la Petición**:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "password123"
}
```

**Respuesta Exitosa** (201):
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "usuario@ejemplo.com"
}
```

**Errores**:
- `400`: Email ya registrado
- `422`: Datos de entrada inválidos

### Inicio de Sesión

**Endpoint**: `POST /auth/login`

**Descripción**: Autentica un usuario y retorna un token JWT.

**Cuerpo de la Petición**:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "password123"
}
```

**Respuesta Exitosa** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores**:
- `401`: Credenciales inválidas
- `422`: Datos de entrada inválidos

## Gestión de Gastos

### Crear Gasto

**Endpoint**: `POST /expenses`

**Descripción**: Crea un nuevo gasto para el usuario autenticado.

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Cuerpo de la Petición**:
```json
{
  "amount": 1500.50,
  "category": "food",
  "description": "Compras del supermercado",
  "date": "2024-01-15T10:30:00Z"
}
```

**Respuesta Exitosa** (201):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "amount": 1500.50,
  "category": "food",
  "description": "Compras del supermercado",
  "date": "2024-01-15T10:30:00Z"
}
```

### Listar Gastos

**Endpoint**: `GET /expenses`

**Descripción**: Obtiene la lista de gastos del usuario autenticado con opciones de filtrado.

**Headers**:
```
Authorization: Bearer <token>
```

**Parámetros de Consulta**:
- `category` (opcional): Filtrar por categoría
- `rango` (opcional): Filtrar por tiempo
- `start_date` (opcional): Fecha de inicio (formato ISO)
- `end_date` (opcional): Fecha de fin (formato ISO)

**Ejemplos de Uso**:
```
GET /expenses                           # Todos los gastos
GET /expenses?category=food             # Solo gastos de comida
GET /expenses?rango=past_week           # Gastos de la última semana
GET /expenses?rango=custom&start_date=2024-01-01T00:00:00Z&end_date=2024-01-31T23:59:59Z
```

**Respuesta Exitosa** (200):
```json
[
  {
    "id": "507f1f77bcf86cd799439012",
    "user_id": "507f1f77bcf86cd799439011",
    "amount": 1500.50,
    "category": "food",
    "description": "Compras del supermercado",
    "date": "2024-01-15T10:30:00Z"
  },
  {
    "id": "507f1f77bcf86cd799439013",
    "user_id": "507f1f77bcf86cd799439011",
    "amount": 250.00,
    "category": "transport",
    "description": "Gasolina",
    "date": "2024-01-14T15:20:00Z"
  }
]
```

### Actualizar Gasto

**Endpoint**: `PATCH /expenses/{id}`

**Descripción**: Actualiza un gasto existente del usuario autenticado.

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Cuerpo de la Petición** (campos opcionales):
```json
{
  "amount": 1800.00,
  "description": "Compras del supermercado (actualizado)"
}
```

**Respuesta Exitosa** (200):
```json
{
  "id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "amount": 1800.00,
  "category": "food",
  "description": "Compras del supermercado (actualizado)",
  "date": "2024-01-15T10:30:00Z"
}
```

### Eliminar Gasto

**Endpoint**: `DELETE /expenses/{id}`

**Descripción**: Elimina un gasto del usuario autenticado.

**Headers**:
```
Authorization: Bearer <token>
```

**Respuesta Exitosa** (204): Sin contenido

**Errores**:
- `404`: Gasto no encontrado
- `403`: No autorizado para eliminar este gasto

## Categorías Disponibles

| Categoría | Descripción |
|-----------|-------------|
| `food` | Alimentación y comidas |
| `transport` | Transporte y movilidad |
| `entertainment` | Entretenimiento y ocio |
| `health` | Salud y bienestar |
| `shopping` | Compras y retail |
| `bills` | Facturas y servicios |
| `other` | Otros gastos |

## Rangos de Tiempo

| Rango | Descripción |
|-------|-------------|
| `past_week` | Últimos 7 días |
| `past_month` | Últimos 30 días |
| `last_3_months` | Últimos 90 días |
| `custom` | Rango personalizado (requiere start_date y end_date) |

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| `400` | Bad Request - Datos de entrada incorrectos |
| `401` | Unauthorized - Token inválido o expirado |
| `403` | Forbidden - No autorizado para la acción |
| `404` | Not Found - Recurso no encontrado |
| `422` | Unprocessable Entity - Validación fallida |
| `500` | Internal Server Error - Error del servidor |

## Ejemplos de Uso

### Flujo Completo

1. **Registrar usuario**:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "password123"}'
```

2. **Iniciar sesión**:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "password123"}'
```

3. **Crear gasto**:
```bash
curl -X POST "http://localhost:8000/expenses" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1500.50, "category": "food", "description": "Compras", "date": "2024-01-15T10:30:00Z"}'
```

4. **Listar gastos**:
```bash
curl -X GET "http://localhost:8000/expenses" \
  -H "Authorization: Bearer <token>"
```

## Rate Limiting

Actualmente no hay límites de rate limiting implementados, pero se recomienda no exceder 100 requests por minuto por usuario.

## Versiones

- **v1.0.0**: Versión inicial con funcionalidades básicas de CRUD
- **Próximas versiones**: Estadísticas avanzadas, exportación de datos, notificaciones
