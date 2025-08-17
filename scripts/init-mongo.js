// Script de inicialización para MongoDB
// Se ejecuta automáticamente al crear el contenedor

// Crear la base de datos de gastos
db = db.getSiblingDB('expenses_db');

// Crear colecciones
db.createCollection('users');
db.createCollection('expenses');

// Crear índices para optimizar consultas
db.users.createIndex({ "email": 1 }, { unique: true });
db.expenses.createIndex({ "user_id": 1, "date": -1 });
db.expenses.createIndex({ "user_id": 1, "category": 1 });
db.expenses.createIndex({ "date": -1 });

print('✅ Base de datos inicializada correctamente');
print('📊 Colecciones creadas: users, expenses');
print('🔍 Índices creados para optimizar consultas');
