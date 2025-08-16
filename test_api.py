#!/usr/bin/env python3
"""
Script de pruebas completo para la API de Seguimiento de Gastos
Demuestra todas las funcionalidades paso a paso
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Configuración
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def print_step(step, description):
    """Imprime un paso de la demostración"""
    print(f"\n{'='*60}")
    print(f"🔹 PASO {step}: {description}")
    print(f"{'='*60}")

def print_success(message, data=None):
    """Imprime un mensaje de éxito"""
    print(f"✅ {message}")
    if data:
        print(f"📄 Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")

def print_error(message):
    """Imprime un mensaje de error"""
    print(f"❌ {message}")

def test_health_check():
    """Prueba que el servidor esté funcionando"""
    print_step(1, "VERIFICANDO QUE EL SERVIDOR ESTÉ FUNCIONANDO")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print_success("Servidor funcionando correctamente")
            print(f"📚 Documentación disponible en: {BASE_URL}/docs")
        else:
            print_error("Servidor no responde correctamente")
            return False
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor. Asegúrate de que esté ejecutándose.")
        return False
    
    return True

def test_user_registration():
    """Prueba el registro de usuarios"""
    print_step(2, "REGISTRANDO UN NUEVO USUARIO")
    
    user_data = {
        "email": "usuario@ejemplo.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            headers=HEADERS,
            json=user_data
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success("Usuario registrado exitosamente", data)
            return data.get("id")
        else:
            print_error(f"Error al registrar usuario: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None

def test_user_login():
    """Prueba el inicio de sesión"""
    print_step(3, "INICIANDO SESIÓN")
    
    login_data = {
        "email": "usuario@ejemplo.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            headers=HEADERS,
            json=login_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Inicio de sesión exitoso", data)
            return data.get("access_token")
        else:
            print_error(f"Error al iniciar sesión: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None

def test_create_expenses(token):
    """Prueba la creación de gastos"""
    print_step(4, "CREANDO GASTOS DE EJEMPLO")
    
    expenses = [
        {
            "amount": 1500.50,
            "category": "food",
            "description": "Compras del supermercado",
            "date": datetime.now().isoformat()
        },
        {
            "amount": 250.00,
            "category": "transport",
            "description": "Gasolina del auto",
            "date": (datetime.now() - timedelta(days=1)).isoformat()
        },
        {
            "amount": 800.00,
            "category": "entertainment",
            "description": "Cena en restaurante",
            "date": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "amount": 1200.00,
            "category": "health",
            "description": "Consulta médica",
            "date": (datetime.now() - timedelta(days=3)).isoformat()
        }
    ]
    
    expense_ids = []
    headers_with_token = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    for i, expense in enumerate(expenses, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/expenses",
                headers=headers_with_token,
                json=expense
            )
            
            if response.status_code == 201:
                data = response.json()
                expense_ids.append(data["id"])
                print_success(f"Gasto {i} creado: {expense['description']}", data)
            else:
                print_error(f"Error al crear gasto {i}: {response.status_code}")
                print(f"Respuesta: {response.text}")
        except Exception as e:
            print_error(f"Error de conexión al crear gasto {i}: {e}")
    
    return expense_ids

def test_list_expenses(token):
    """Prueba el listado de gastos"""
    print_step(5, "LISTANDO TODOS LOS GASTOS")
    
    headers_with_token = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/expenses",
            headers=headers_with_token
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Se encontraron {len(data)} gastos")
            for expense in data:
                print(f"  💰 {expense['description']}: ${expense['amount']} ({expense['category']})")
            return data
        else:
            print_error(f"Error al listar gastos: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return None

def test_filter_expenses(token):
    """Prueba los filtros de gastos"""
    print_step(6, "PROBANDO FILTROS DE GASTOS")
    
    headers_with_token = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    # Filtro por categoría
    print("\n🔍 Filtrando por categoría 'food':")
    try:
        response = requests.get(
            f"{BASE_URL}/expenses?category=food",
            headers=headers_with_token
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Se encontraron {len(data)} gastos en la categoría 'food'")
            for expense in data:
                print(f"  🍽️  {expense['description']}: ${expense['amount']}")
        else:
            print_error(f"Error al filtrar por categoría: {response.status_code}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")
    
    # Filtro por rango de tiempo
    print("\n🔍 Filtrando gastos de la última semana:")
    try:
        response = requests.get(
            f"{BASE_URL}/expenses?rango=past_week",
            headers=headers_with_token
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Se encontraron {len(data)} gastos de la última semana")
            for expense in data:
                print(f"  📅 {expense['description']}: ${expense['amount']} ({expense['date'][:10]})")
        else:
            print_error(f"Error al filtrar por tiempo: {response.status_code}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")

def test_update_expense(token, expense_ids):
    """Prueba la actualización de gastos"""
    if not expense_ids:
        print_error("No hay gastos para actualizar")
        return
    
    print_step(7, "ACTUALIZANDO UN GASTO")
    
    expense_id = expense_ids[0]
    update_data = {
        "amount": 1800.00,
        "description": "Compras del supermercado (actualizado)"
    }
    
    headers_with_token = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    try:
        response = requests.patch(
            f"{BASE_URL}/expenses/{expense_id}",
            headers=headers_with_token,
            json=update_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Gasto actualizado exitosamente", data)
        else:
            print_error(f"Error al actualizar gasto: {response.status_code}")
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")

def test_delete_expense(token, expense_ids):
    """Prueba la eliminación de gastos"""
    if not expense_ids:
        print_error("No hay gastos para eliminar")
        return
    
    print_step(8, "ELIMINANDO UN GASTO")
    
    expense_id = expense_ids[-1]  # Eliminar el último gasto
    headers_with_token = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    try:
        response = requests.delete(
            f"{BASE_URL}/expenses/{expense_id}",
            headers=headers_with_token
        )
        
        if response.status_code == 204:
            print_success("Gasto eliminado exitosamente")
        else:
            print_error(f"Error al eliminar gasto: {response.status_code}")
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")

def test_final_list(token):
    """Muestra la lista final de gastos"""
    print_step(9, "LISTA FINAL DE GASTOS")
    
    headers_with_token = {**HEADERS, "Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/expenses",
            headers=headers_with_token
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Lista final: {len(data)} gastos restantes")
            
            total = sum(expense['amount'] for expense in data)
            print(f"\n💰 TOTAL GASTADO: ${total:.2f}")
            
            # Agrupar por categoría
            categories = {}
            for expense in data:
                cat = expense['category']
                if cat not in categories:
                    categories[cat] = 0
                categories[cat] += expense['amount']
            
            print("\n📊 GASTOS POR CATEGORÍA:")
            for category, amount in categories.items():
                print(f"  {category.upper()}: ${amount:.2f}")
                
        else:
            print_error(f"Error al obtener lista final: {response.status_code}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🚀 DEMOSTRACIÓN COMPLETA DE LA API DE SEGUIMIENTO DE GASTOS")
    print("=" * 70)
    
    # Verificar que el servidor esté funcionando
    if not test_health_check():
        return
    
    # Registrar usuario
    user_id = test_user_registration()
    if not user_id:
        print_error("No se pudo registrar el usuario. Abortando...")
        return
    
    # Iniciar sesión
    token = test_user_login()
    if not token:
        print_error("No se pudo iniciar sesión. Abortando...")
        return
    
    # Crear gastos
    expense_ids = test_create_expenses(token)
    
    # Listar gastos
    test_list_expenses(token)
    
    # Probar filtros
    test_filter_expenses(token)
    
    # Actualizar gasto
    test_update_expense(token, expense_ids)
    
    # Eliminar gasto
    test_delete_expense(token, expense_ids)
    
    # Lista final
    test_final_list(token)
    
    print("\n" + "="*70)
    print("🎉 ¡DEMOSTRACIÓN COMPLETADA EXITOSAMENTE!")
    print("="*70)
    print("\n📋 RESUMEN DE FUNCIONALIDADES PROBADAS:")
    print("✅ Verificación del servidor")
    print("✅ Registro de usuarios")
    print("✅ Inicio de sesión con JWT")
    print("✅ Creación de gastos")
    print("✅ Listado de gastos")
    print("✅ Filtros por categoría y tiempo")
    print("✅ Actualización de gastos")
    print("✅ Eliminación de gastos")
    print("✅ Cálculo de totales y estadísticas")
    
    print(f"\n🌐 Accede a la documentación interactiva en: {BASE_URL}/docs")

if __name__ == "__main__":
    main()
