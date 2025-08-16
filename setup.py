#!/usr/bin/env python3
"""
Script de configuración rápida para la API de Seguimiento de Gastos
"""

import os
import shutil
from pathlib import Path

def main():
    print("🔧 Configurando API de Seguimiento de Gastos...")
    
    # Verificar si existe el archivo .env
    env_file = Path(".env")
    example_file = Path("config.env.example")
    
    if not env_file.exists() and example_file.exists():
        print("📝 Creando archivo .env desde el ejemplo...")
        shutil.copy(example_file, env_file)
        print("✅ Archivo .env creado exitosamente")
        print("⚠️  IMPORTANTE: Edita el archivo .env y cambia el JWT_SECRET por seguridad")
    elif env_file.exists():
        print("✅ El archivo .env ya existe")
    else:
        print("❌ No se encontró el archivo de ejemplo config.env.example")
        return
    
    print("\n🚀 Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Asegúrate de que MongoDB esté ejecutándose")
    print("2. Edita el archivo .env si es necesario")
    print("3. Ejecuta: python start.py")
    print("4. Visita: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
