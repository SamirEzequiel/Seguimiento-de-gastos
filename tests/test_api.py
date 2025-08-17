"""
Tests unitarios para la API de Seguimiento de Gastos
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import json

from app.main import app

client = TestClient(app)

class TestAuth:
    """Tests para endpoints de autenticación"""
    
    def test_register_user(self):
        """Test registro de usuario"""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["email"] == user_data["email"]
    
    def test_register_duplicate_user(self):
        """Test registro de usuario duplicado"""
        user_data = {
            "email": "duplicate@example.com",
            "password": "testpassword123"
        }
        
        # Primer registro
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 201
        
        # Segundo registro con mismo email
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
    
    def test_login_user(self):
        """Test inicio de sesión"""
        # Primero registrar usuario
        user_data = {
            "email": "login@example.com",
            "password": "testpassword123"
        }
        client.post("/auth/register", json=user_data)
        
        # Luego hacer login
        response = client.post("/auth/login", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test login con credenciales inválidas"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401

class TestExpenses:
    """Tests para endpoints de gastos"""
    
    @pytest.fixture
    def auth_token(self):
        """Fixture para obtener token de autenticación"""
        # Registrar y hacer login
        user_data = {
            "email": "expenses@example.com",
            "password": "testpassword123"
        }
        client.post("/auth/register", json=user_data)
        
        response = client.post("/auth/login", json=user_data)
        data = response.json()
        return data["access_token"]
    
    def test_create_expense(self, auth_token):
        """Test creación de gasto"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        expense_data = {
            "amount": 100.50,
            "category": "food",
            "description": "Test expense",
            "date": datetime.now().isoformat()
        }
        
        response = client.post("/expenses", json=expense_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["amount"] == expense_data["amount"]
        assert data["category"] == expense_data["category"]
        assert data["description"] == expense_data["description"]
    
    def test_create_expense_unauthorized(self):
        """Test creación de gasto sin autenticación"""
        expense_data = {
            "amount": 100.50,
            "category": "food",
            "description": "Test expense",
            "date": datetime.now().isoformat()
        }
        
        response = client.post("/expenses", json=expense_data)
        assert response.status_code == 401
    
    def test_list_expenses(self, auth_token):
        """Test listado de gastos"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Crear algunos gastos
        expense_data = {
            "amount": 100.50,
            "category": "food",
            "description": "Test expense 1",
            "date": datetime.now().isoformat()
        }
        client.post("/expenses", json=expense_data, headers=headers)
        
        expense_data2 = {
            "amount": 200.00,
            "category": "transport",
            "description": "Test expense 2",
            "date": datetime.now().isoformat()
        }
        client.post("/expenses", json=expense_data2, headers=headers)
        
        # Listar gastos
        response = client.get("/expenses", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 2
    
    def test_filter_expenses_by_category(self, auth_token):
        """Test filtrado por categoría"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Crear gastos de diferentes categorías
        expense_data = {
            "amount": 100.50,
            "category": "food",
            "description": "Food expense",
            "date": datetime.now().isoformat()
        }
        client.post("/expenses", json=expense_data, headers=headers)
        
        expense_data2 = {
            "amount": 200.00,
            "category": "transport",
            "description": "Transport expense",
            "date": datetime.now().isoformat()
        }
        client.post("/expenses", json=expense_data2, headers=headers)
        
        # Filtrar por categoría food
        response = client.get("/expenses?category=food", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert all(expense["category"] == "food" for expense in data)
    
    def test_update_expense(self, auth_token):
        """Test actualización de gasto"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Crear gasto
        expense_data = {
            "amount": 100.50,
            "category": "food",
            "description": "Original description",
            "date": datetime.now().isoformat()
        }
        response = client.post("/expenses", json=expense_data, headers=headers)
        expense_id = response.json()["id"]
        
        # Actualizar gasto
        update_data = {
            "amount": 150.00,
            "description": "Updated description"
        }
        response = client.patch(f"/expenses/{expense_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["amount"] == update_data["amount"]
        assert data["description"] == update_data["description"]
    
    def test_delete_expense(self, auth_token):
        """Test eliminación de gasto"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Crear gasto
        expense_data = {
            "amount": 100.50,
            "category": "food",
            "description": "To be deleted",
            "date": datetime.now().isoformat()
        }
        response = client.post("/expenses", json=expense_data, headers=headers)
        expense_id = response.json()["id"]
        
        # Eliminar gasto
        response = client.delete(f"/expenses/{expense_id}", headers=headers)
        assert response.status_code == 204
        
        # Verificar que fue eliminado
        response = client.get(f"/expenses/{expense_id}", headers=headers)
        assert response.status_code == 404

class TestValidation:
    """Tests para validación de datos"""
    
    def test_invalid_email_format(self):
        """Test email con formato inválido"""
        user_data = {
            "email": "invalid-email",
            "password": "testpassword123"
        }
        
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422
    
    def test_invalid_expense_amount(self):
        """Test monto de gasto inválido"""
        # Primero obtener token
        user_data = {
            "email": "validation@example.com",
            "password": "testpassword123"
        }
        client.post("/auth/register", json=user_data)
        response = client.post("/auth/login", json=user_data)
        token = response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        expense_data = {
            "amount": -100,  # Monto negativo
            "category": "food",
            "description": "Test expense",
            "date": datetime.now().isoformat()
        }
        
        response = client.post("/expenses", json=expense_data, headers=headers)
        assert response.status_code == 422
    
    def test_invalid_category(self):
        """Test categoría inválida"""
        # Primero obtener token
        user_data = {
            "email": "category@example.com",
            "password": "testpassword123"
        }
        client.post("/auth/register", json=user_data)
        response = client.post("/auth/login", json=user_data)
        token = response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        expense_data = {
            "amount": 100.50,
            "category": "invalid_category",
            "description": "Test expense",
            "date": datetime.now().isoformat()
        }
        
        response = client.post("/expenses", json=expense_data, headers=headers)
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__])
