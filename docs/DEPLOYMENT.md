# 🚀 Guía de Despliegue

## Opciones de Despliegue

### 1. Despliegue Local

#### Prerrequisitos
- Python 3.11+
- MongoDB 6.0+
- Git

#### Pasos
```bash
# Clonar repositorio
git clone <tu-repositorio>
cd Seguimiento-de-gastos

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp config.env.example .env
# Editar .env con tus configuraciones

# Iniciar MongoDB
# Asegúrate de que MongoDB esté ejecutándose

# Ejecutar aplicación
python start.py
```

### 2. Despliegue con Docker

#### Prerrequisitos
- Docker
- Docker Compose

#### Pasos
```bash
# Clonar repositorio
git clone <tu-repositorio>
cd Seguimiento-de-gastos

# Construir y ejecutar con Docker Compose
docker-compose up -d

# Verificar servicios
docker-compose ps
```

#### Acceso
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- MongoDB Express: http://localhost:8081

### 3. Despliegue en Producción

#### Variables de Entorno de Producción
```env
# Configuración de MongoDB
MONGO_URI=mongodb://usuario:password@tu-servidor-mongodb:27017
MONGO_DB=expenses_prod

# Configuración de JWT
JWT_SECRET=secreto-super-seguro-de-produccion-cambiame
JWT_ALG=HS256
JWT_EXPIRES_MIN=1440  # 24 horas

# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# Configuración adicional
LOG_LEVEL=INFO
CORS_ORIGINS=https://tu-dominio.com
```

#### Configuración de Nginx (Opcional)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Configuración de SSL (Recomendado)
```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com
```

### 4. Despliegue en la Nube

#### Heroku
```bash
# Crear aplicación en Heroku
heroku create tu-app-name

# Configurar variables de entorno
heroku config:set MONGO_URI=mongodb://...
heroku config:set JWT_SECRET=tu-secreto
heroku config:set JWT_EXPIRES_MIN=1440

# Desplegar
git push heroku main
```

#### AWS EC2
```bash
# Conectar a instancia EC2
ssh -i tu-key.pem ubuntu@tu-ip

# Instalar dependencias
sudo apt update
sudo apt install python3 python3-pip nginx

# Clonar y configurar aplicación
git clone <tu-repositorio>
cd Seguimiento-de-gastos
pip3 install -r requirements.txt

# Configurar como servicio systemd
sudo nano /etc/systemd/system/expenses-api.service
```

#### Google Cloud Run
```bash
# Construir imagen
gcloud builds submit --tag gcr.io/tu-proyecto/expenses-api

# Desplegar
gcloud run deploy expenses-api \
  --image gcr.io/tu-proyecto/expenses-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Monitoreo y Logs

### Logs de la Aplicación
```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Ver logs específicos
docker-compose logs api | grep ERROR
```

### Métricas de Rendimiento
- Tiempo de respuesta promedio
- Número de requests por minuto
- Uso de memoria y CPU
- Errores por endpoint

### Health Checks
```bash
# Verificar estado de la API
curl http://localhost:8000/docs

# Verificar conexión a MongoDB
# Los logs mostrarán errores de conexión si hay problemas
```

## Seguridad

### Configuraciones Recomendadas
1. **Cambiar JWT_SECRET** en producción
2. **Configurar CORS** apropiadamente
3. **Usar HTTPS** en producción
4. **Configurar rate limiting**
5. **Validar inputs** (ya implementado con Pydantic)
6. **Usar variables de entorno** para configuraciones sensibles

### Firewall
```bash
# Configurar firewall (Ubuntu/Debian)
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## Backup y Recuperación

### Backup de MongoDB
```bash
# Backup completo
mongodump --uri="mongodb://localhost:27017/expenses_db" --out=/backup

# Restaurar backup
mongorestore --uri="mongodb://localhost:27017/expenses_db" /backup/expenses_db
```

### Backup Automático (Cron)
```bash
# Crear script de backup
nano /usr/local/bin/backup-expenses.sh

# Hacer ejecutable
chmod +x /usr/local/bin/backup-expenses.sh

# Configurar cron job
crontab -e
# Añadir: 0 2 * * * /usr/local/bin/backup-expenses.sh
```

## Escalabilidad

### Horizontal Scaling
- Usar load balancer (nginx, haproxy)
- Configurar múltiples instancias de la API
- Usar MongoDB replica set para la base de datos

### Vertical Scaling
- Aumentar recursos de la instancia
- Optimizar consultas de MongoDB
- Implementar caching (Redis)

## Troubleshooting

### Problemas Comunes

#### Error de Conexión a MongoDB
```bash
# Verificar que MongoDB esté ejecutándose
sudo systemctl status mongod

# Verificar conectividad
telnet localhost 27017
```

#### Error de Puerto en Uso
```bash
# Verificar puertos en uso
netstat -tulpn | grep :8000

# Cambiar puerto en .env
PORT=8001
```

#### Error de Permisos
```bash
# Verificar permisos de archivos
ls -la

# Corregir permisos
chmod 644 .env
chmod +x start.py
```

### Logs de Debug
```bash
# Ejecutar con logs detallados
uvicorn app.main:app --reload --log-level debug
```

## Contacto y Soporte

Para problemas de despliegue:
- Revisar logs de la aplicación
- Verificar configuración de variables de entorno
- Consultar documentación de FastAPI y MongoDB
- Abrir issue en el repositorio del proyecto
