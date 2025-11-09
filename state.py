"""
Este módulo define la estructura del estado (`ResearchState`) que se utiliza
para mantener y pasar información a través de los nodos del grafo de LangGraph.
"""

from typing import List, TypedDict

class ResearchState(TypedDict):
    """
    Representa el estado actual del proceso de investigación.

    Atributos:
        topic (str): El tema principal de la investigación, proporcionado como entrada inicial.
        queries (List[str]): Una lista de consultas de búsqueda generadas para buscar información.
        raw_results (List[str]): Una lista de resultados "crudos" obtenidos de las búsquedas
                                 (en este caso, simulados como "mock papers").
        iteration_count (int): Un contador para rastrear el número de iteraciones en el grafo,
                               útil para prevenir bucles infinitos y simular el progreso.
        is_sufficient (bool): Una bandera booleana que indica si los resultados de la investigación
                              se consideran suficientes para generar un informe final.
        report_draft (str): El borrador actual del informe de investigación que se está construyendo.
        human_feedback (str): Simula la retroalimentación humana, que puede ser 'approve' para
                              aceptar el informe, o 'retry' para solicitar más investigación.
    """
    topic: str
    queries: List[str]
    raw_results: List[str]
    iteration_count: int
    is_sufficient: bool
    report_draft: str
    human_feedback: str
