#!/usr/bin/env python3
"""
Script de inicio para la API de Seguimiento de Gastos
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno
    load_dotenv()
    
    # Configuración del servidor
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Iniciando API de Seguimiento de Gastos...")
    print(f"📡 Servidor: http://{host}:{port}")
    print(f"📚 Documentación: http://{host}:{port}/docs")
    print(f"🔧 Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    # Iniciar servidor
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
