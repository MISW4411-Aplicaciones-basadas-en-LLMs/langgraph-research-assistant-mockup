"""
Este módulo contiene funciones de utilidad generales para el proyecto,
como la simulación de cargas o retrasos.
"""

import sys
import time

def simular_carga(segundos: int = 3, mensaje: str = "Procesando"):
    """
    Simula un retraso con una barra de carga animada en la consola.

    Args:
        segundos (int): La duración total de la simulación en segundos. Por defecto es 3.
        mensaje (str): El mensaje a mostrar antes de la barra de carga. Por defecto es "Procesando".
    """
    ancho_barra = 30
    intervalo = segundos / ancho_barra
    
    sys.stdout.write(f"\n{mensaje} [")
    sys.stdout.flush()
    
    for _ in range(ancho_barra):
        time.sleep(intervalo)
        sys.stdout.write("=")
        sys.stdout.flush()
    
    sys.stdout.write("] Listo!\n")
    sys.stdout.flush()
    time.sleep(0.5)
