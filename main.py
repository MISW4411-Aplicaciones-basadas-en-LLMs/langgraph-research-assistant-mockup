"""
Este es el archivo que define y ejecuta el grafo de LangGraph
para un asistente de investigación simulado.

El grafo orquesta una serie de nodos para generar consultas, buscar información,
evaluar resultados, refinar la búsqueda, sintetizar informes y solicitar
aprobación humana.
"""

import operator
from typing import Annotated, List, Literal, Union
from langgraph.graph import END, START, StateGraph

from utils import simular_carga
from state import ResearchState
from graph_utils import save_graph_image

# --- Nodos del Grafo (Mockups Funcionales) ---
def node_generate_queries(state: ResearchState) -> ResearchState:
    """
    Nodo que simula la generación de consultas de búsqueda iniciales
    basadas en el tema de investigación.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        ResearchState: El estado actualizado con las nuevas consultas y el contador de iteración.
    """
    simular_carga(3, "Iniciando motor de razonamiento")
    print(f"\n\n===== [node_generate_queries] =====\n")
    print(f"   - Tema de Investigación: '{state['topic']}'")
    
    # Simulación de LLM generando queries
    new_queries = [f"principios {state['topic']}", f"avances recientes {state['topic']}", f"{state['topic']} metodología"]
    print(f"   - Consultas Generadas: {new_queries}")
    return {
        "queries": new_queries,
        "iteration_count": 0,
        "human_feedback": "pending" # Reset del feedback al iniciar/reiniciar
    }

def node_search_api(state: ResearchState) -> ResearchState:
    """
    Nodo que simula la consulta a una API académica para obtener resultados.
    La cantidad de resultados varía según la iteración para simular un proceso de refinamiento.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        ResearchState: El estado actualizado con los resultados "crudos" de la búsqueda.
    """
    simular_carga(3, "Consultando bases de datos externas")
    print(f"\n\n===== [node_search_api] =====\n")
    print(f"   - Ejecutando Consultas: {state['queries']}")
    
    # Simulación de resultados. Devuelve pocos resultados en la primera iteración (count 0)
    if state["iteration_count"] == 0:
        results = ["Paper A (muy antiguo)", "Paper B (poco relevante)"]
    else:
        results = ["Paper A", "Paper B", "Paper C (relevante, 2024)", "Paper D (survey seminal)"]

    print(f"   - Resultados Encontrados: {len(results)} documentos.")
    return {"raw_results": results}

def node_evaluate_results(state: ResearchState) -> ResearchState:
    """
    Nodo que evalúa automáticamente la suficiencia de los resultados de la búsqueda.
    Incrementa el contador de iteraciones.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        ResearchState: El estado actualizado con la bandera `is_sufficient` y el contador de iteración.
    """
    simular_carga(2, "Analizando relevancia")
    print(f"\n\n===== [node_evaluate_results] =====\n")
    
    # Lógica simulada: Necesitamos al menos 3 papers buenos.
    # En iteración 0, tenemos 2 (fallará). En iteración 1, tenemos 4 (pasará).
    is_sufficient = len(state["raw_results"]) >= 3

    if not is_sufficient:
        print("   - Evaluación: INSUFICIENTE. Se requiere refinamiento.")
    else:
        print("   - Evaluación: SUFICIENTE. Procediendo a síntesis.")

    return {
        "is_sufficient": is_sufficient,
        "iteration_count": state["iteration_count"] + 1
    }

def node_refine_search(state: ResearchState) -> ResearchState:
    """
    Nodo que simula el refinamiento de las consultas de búsqueda para obtener mejores resultados.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        ResearchState: El estado actualizado con las consultas de búsqueda refinadas.
    """
    simular_carga(2, "Ajustando parámetros de búsqueda")
    print(f"\n\n===== [node_refine_search] =====\n")
    
    # Simula hacer las queries más específicas
    new_queries = [q + " review" for q in state["queries"]]
    print(f"   - Nuevas Consultas Generadas: {len(new_queries)}")
    return {"queries": new_queries}

def node_synthesize_report(state: ResearchState) -> ResearchState:
    """
    Nodo que simula la síntesis de un borrador de informe basado en los resultados obtenidos.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        ResearchState: El estado actualizado con el borrador del informe.
    """
    simular_carga(4, "Redactando informe final")
    print(f"\n\n===== [node_synthesize_report] =====\n")
    draft = f"INFORME SOBRE {state['topic'].upper()}\nBasado en {len(state['raw_results'])} papers clave, el campo muestra..."
    print("   - Borrador de Informe Generado.")
    return {"report_draft": draft}

def node_human_approval(state: ResearchState) -> ResearchState:
    """
    Nodo que simula un paso de aprobación humana para el informe.
    En un sistema real, esto podría pausar la ejecución para la intervención del usuario.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        ResearchState: El estado actualizado con la retroalimentación humana simulada ('approve').
    """
    simular_carga(1, "Preparando interfaz de revisión")
    print(f"\n\n===== [node_human_approval] =====\n")
    print(f"   - Mostrando borrador al usuario para revisión:\n\n{state['report_draft']}\n")
    
    # NOTA: En un sistema real, aquí usaríamos `interrupt` para pausar la ejecución.
    # Para este mockup script, simulamos una aprobación automática.
    simular_carga(2, "Esperando input del usuario")
    print("\n   >>> [Simulación] Usuario revisando... APROBADO.\n")
    return {"human_feedback": "approve"}

# --- Lógica Condicional (Routers) ---
def route_evaluation(state: ResearchState) -> Literal["synthesize_report", "refine_search"]:
    """
    Router que decide el siguiente paso basado en la suficiencia de los resultados.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        Literal["synthesize_report", "refine_search"]: El nombre del siguiente nodo.
    """
    if state["is_sufficient"]:
        return "synthesize_report"
    return "refine_search"

def route_human_feedback(state: ResearchState) -> Literal[END, "generate_queries"]:
    """
    Router que decide si el proceso termina o se reinicia basado en la retroalimentación humana.

    Args:
        state (ResearchState): El estado actual del grafo.

    Returns:
        Literal[END, "generate_queries"]: El nombre del siguiente nodo o END para finalizar.
    """
    if state["human_feedback"] == "approve":
        print("\n\n===== PROCESO FINALIZADO CON ÉXITO =====\n")
        print("   - Informe entregado satisfactoriamente.\n")
        return END
    print("\n\n===== FEEDBACK NEGATIVO =====\n")
    print("   - Reiniciando proceso de investigación.\n")
    return "generate_queries"

# --- Construcción del Grafo ---
builder = StateGraph(ResearchState)

# Añadir nodos
builder.add_node("generate_queries", node_generate_queries)
builder.add_node("search_api", node_search_api)
builder.add_node("evaluate_results", node_evaluate_results)
builder.add_node("refine_search", node_refine_search)
builder.add_node("synthesize_report", node_synthesize_report)
builder.add_node("human_approval", node_human_approval)

# Definir flujo principal
builder.add_edge(START, "generate_queries")
builder.add_edge("generate_queries", "search_api")
builder.add_edge("search_api", "evaluate_results")

# Bifurcación 1: Evaluación automática
builder.add_conditional_edges(
    "evaluate_results",
    route_evaluation
)

# Ciclo de refinamiento
builder.add_edge("refine_search", "search_api")

# Flujo hacia aprobación
builder.add_edge("synthesize_report", "human_approval")

# Bifurcación 2: Aprobación humana (puede reiniciar o terminar)
builder.add_conditional_edges(
    "human_approval",
    route_human_feedback
)

# Compilar el grafo
graph = builder.compile()

# --- Ejecución y Visualización ---
save_graph_image(graph, "research_assistant_mockup.png")

initial_state = ResearchState(
    topic = "Impacto de la IA generativa en la educación superior",
    queries = [], raw_results = [], iteration_count = 0,
    is_sufficient = False, report_draft="", human_feedback = "pending"
)

print("\n\n************************************************")
print("***** Iniciando Asistente de Investigación *****")
print("************************************************\n")
final_state = graph.invoke(
    initial_state,
    config={"tags": ["research_workflow", "generative_ai_education"]}
)
