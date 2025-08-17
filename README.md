# 💰 API de Seguimiento de Gastos

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6+-yellow.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> API REST moderna y escalable para el seguimiento de gastos personales, desarrollada con FastAPI y MongoDB.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API Reference](#-api-reference)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

- 🔐 **Autenticación JWT** - Sistema seguro de autenticación
- 💰 **Gestión de Gastos** - CRUD completo para gastos
- 📊 **Categorización** - Organización por categorías predefinidas
- 🔍 **Filtros Avanzados** - Por fecha, categoría y rangos de tiempo
- 📈 **Estadísticas** - Totales y análisis por categoría
- 🗄️ **Base de Datos NoSQL** - MongoDB para escalabilidad
- 📝 **Documentación Automática** - Swagger/OpenAPI integrado
- 🚀 **Alta Performance** - FastAPI con async/await
- 🛡️ **Validación de Datos** - Pydantic para type safety

## 🛠️ Tecnologías

- **Backend**: FastAPI 0.115.0
- **Base de Datos**: MongoDB 6+
- **Autenticación**: JWT (PyJWT)
- **Validación**: Pydantic 2.8.2
- **Servidor**: Uvicorn 0.30.6
- **Hashing**: Passlib + bcrypt
- **Configuración**: Pydantic Settings

## 🚀 Instalación

### Prerrequisitos

- Python 3.11 o superior
- MongoDB 6.0 o superior
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd Seguimiento-de-gastos
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
```

3. **Activar entorno virtual**
```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración de MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB=expenses_db

# Configuración de JWT
JWT_SECRET=tu-secreto-super-seguro-aqui-cambialo-en-produccion
JWT_ALG=HS256
JWT_EXPIRES_MIN=60

# Configuración del servidor
HOST=0.0.0.0
PORT=8000
```

### Configuración Rápida

Ejecuta el script de configuración automática:

```bash
python setup.py
```

## 🎯 Uso

### Iniciar el Servidor

```bash
# Opción 1: Script personalizado
python start.py

# Opción 2: Uvicorn directo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Acceder a la Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Ejecutar Pruebas

```bash
# Demostración completa de funcionalidades
python test_api.py
```

## 📚 API Reference

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/auth/register` | Registro de usuarios |
| `POST` | `/auth/login` | Inicio de sesión |

### Gestión de Gastos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/expenses` | Crear nuevo gasto |
| `GET` | `/expenses` | Listar gastos (con filtros) |
| `PATCH` | `/expenses/{id}` | Actualizar gasto |
| `DELETE` | `/expenses/{id}` | Eliminar gasto |

### Parámetros de Filtrado

- `category`: Filtrar por categoría (food, transport, entertainment, health, etc.)
- `rango`: Filtrar por tiempo (past_week, past_month, last_3_months, custom)
- `start_date` / `end_date`: Fechas personalizadas (formato ISO)

### Categorías Disponibles

- `food` - Alimentación
- `transport` - Transporte
- `entertainment` - Entretenimiento
- `health` - Salud
- `shopping` - Compras
- `bills` - Facturas
- `other` - Otros

## 📁 Estructura del Proyecto

```
Seguimiento-de-gastos/
├── app/                    # Código principal de la aplicación
│   ├── __init__.py
│   ├── main.py            # Aplicación FastAPI y endpoints
│   ├── auth.py            # Autenticación y autorización
│   ├── models.py          # Modelos de datos
│   ├── schemas.py         # Esquemas Pydantic
│   ├── db.py             # Configuración de base de datos
│   ├── config.py         # Configuración de la aplicación
│   ├── deps.py           # Dependencias y middleware
│   └── utils.py          # Utilidades y helpers
├── docs/                  # Documentación adicional
├── tests/                 # Tests unitarios e integración
├── scripts/               # Scripts de utilidad
├── .env                   # Variables de entorno (no versionado)
├── .gitignore            # Archivos ignorados por Git
├── requirements.txt      # Dependencias de Python
├── README.md             # Este archivo
├── LICENSE               # Licencia del proyecto
├── start.py              # Script de inicio del servidor
├── setup.py              # Script de configuración
└── test_api.py           # Script de pruebas/demostración
```

## 🔧 Desarrollo

### Estructura de Datos

#### Usuario
```json
{
  "id": "string",
  "email": "string",
  "password": "string (hasheada)"
}
```

#### Gasto
```json
{
  "id": "string",
  "user_id": "string",
  "amount": "number",
  "category": "string",
  "description": "string",
  "date": "datetime"
}
```

### Flujo de Autenticación

1. **Registro**: `POST /auth/register`
2. **Login**: `POST /auth/login` → Retorna JWT token
3. **Autorización**: Incluir `Authorization: Bearer <token>` en headers

## 🧪 Testing

### Pruebas Automatizadas

```bash
# Ejecutar todas las pruebas
python -m pytest

# Ejecutar con cobertura
python -m pytest --cov=app
```

### Pruebas Manuales

```bash
# Demostración completa
python test_api.py
```

## 📊 Monitoreo y Logs

### Logs de la Aplicación

Los logs se muestran en la consola con diferentes niveles:
- `INFO`: Información general
- `WARNING`: Advertencias
- `ERROR`: Errores
- `DEBUG`: Información de depuración

### Métricas

- Tiempo de respuesta de endpoints
- Número de requests por minuto
- Errores por endpoint

## 🚀 Despliegue

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de Entorno de Producción

```env
MONGO_URI=mongodb://tu-servidor-mongodb:27017
MONGO_DB=expenses_prod
JWT_SECRET=secreto-super-seguro-de-produccion
JWT_EXPIRES_MIN=1440  # 24 horas
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Sigue las convenciones de código PEP 8
- Añade tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Verifica que todos los tests pasen


**Desarrollado por Samir Goede**

