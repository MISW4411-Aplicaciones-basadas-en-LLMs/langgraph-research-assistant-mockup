"""
Este módulo contiene funciones de utilidad relacionadas con la visualización
y manipulación del grafo de LangGraph.
"""

from PIL import Image
import io
from langgraph.graph import StateGraph

def save_graph_image(graph: StateGraph, filename: str = "research_assistant_mockup.png"):
    """
    Genera y guarda una imagen del grafo de LangGraph en formato PNG.

    Args:
        graph (StateGraph): La instancia del grafo de LangGraph a visualizar.
        filename (str): El nombre del archivo donde se guardará la imagen.
                        Por defecto es "research_assistant_mockup.png".
    """
    try:
        image_bytes = graph.get_graph().draw_mermaid_png()
        image = Image.open(io.BytesIO(image_bytes))
        image.save(filename)
    except Exception as e:
        print(f"(No se pudo generar la imagen del grafo por falta de dependencias opcionales o error: {e})")
