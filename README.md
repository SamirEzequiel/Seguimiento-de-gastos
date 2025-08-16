# Seguimiento-de-gastos Expenses API

API REST para el seguimiento de gastos personales desarrollada con FastAPI y MongoDB.

## Características

- 🔐 Autenticación JWT
- 💰 Gestión de gastos por categorías
- 📊 Filtros por fechas y categorías
- 🗄️ Base de datos MongoDB
- 📝 Documentación automática con Swagger

## Requisitos

- Python 3.11+
- MongoDB 6+

## Instalación

1. **Clona el repositorio**
```bash
git clone <tu-repositorio>
cd Seguimiento-de-gastos
```

2. **Crea un entorno virtual**
```bash
python -m venv .venv
```

3. **Activa el entorno virtual**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

5. **Configura las variables de entorno**
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

6. **Inicia MongoDB**
Asegúrate de que MongoDB esté ejecutándose en tu sistema.

## Uso

### Iniciar el servidor
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Acceder a la documentación
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints principales

- `POST /auth/register` - Registro de usuarios
- `POST /auth/login` - Inicio de sesión
- `POST /expenses` - Crear gasto
- `GET /expenses` - Listar gastos
- `PATCH /expenses/{id}` - Actualizar gasto
- `DELETE /expenses/{id}` - Eliminar gasto

## Estructura del proyecto

```
app/
├── main.py          # Aplicación principal y endpoints
├── auth.py          # Autenticación y autorización
├── models.py        # Modelos de datos
├── schemas.py       # Esquemas Pydantic
├── db.py           # Configuración de base de datos
├── config.py       # Configuración de la aplicación
├── deps.py         # Dependencias
└── utils.py        # Utilidades
```
