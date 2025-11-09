# Asistente de Investigación con LangGraph (Mockup)

Este proyecto es un mockup funcional de un asistente de investigación automatizado, construido utilizando la biblioteca LangGraph. Simula un flujo de trabajo de investigación que incluye la generación de consultas, búsqueda en APIs académicas, evaluación de resultados, refinamiento de la búsqueda, síntesis de informes preliminares y un paso de aprobación humana.

## Características

El asistente opera a través de una serie de nodos interconectados en un grafo de estado:

*   **`node_generate_queries`**: Genera consultas de búsqueda iniciales basadas en un tema de investigación dado.
*   **`node_search_api`**: Simula la consulta a una API académica para obtener resultados "crudos". La cantidad de resultados puede variar para simular un proceso de refinamiento.
*   **`node_evaluate_results`**: Evalúa automáticamente la suficiencia de los resultados de la búsqueda. Decide si se necesita más refinamiento o si se puede proceder a la síntesis.
*   **`node_refine_search`**: Refina las consultas de búsqueda para intentar obtener resultados más relevantes en iteraciones posteriores.
*   **`node_synthesize_report`**: Sintetiza un borrador de informe basado en los resultados obtenidos.
*   **`node_human_approval`**: Simula un paso de aprobación humana para el informe. En un sistema real, esto podría pausar la ejecución para la intervención del usuario.

## Estructura del Grafo

El grafo define el siguiente flujo:

1.  **Inicio** -> **Generar Consultas**
2.  **Generar Consultas** -> **Buscar en API**
3.  **Buscar en API** -> **Evaluar Resultados**
4.  **Evaluación Condicional**:
    *   Si los resultados son **suficientes**, va a **Sintetizar Informe**.
    *   Si los resultados son **insuficientes**, va a **Refinar Búsqueda**.
5.  **Refinar Búsqueda** -> Vuelve a **Buscar en API** (ciclo de refinamiento).
6.  **Sintetizar Informe** -> **Aprobación Humana**.
7.  **Aprobación Humana Condicional**:
    *   Si el informe es **aprobado**, el proceso **termina**.
    *   Si el informe es **rechazado** (simulado), el proceso **reinicia** desde **Generar Consultas**.

## Uso

Para ejecutar el asistente de investigación simulado, simplemente ejecute el script `main.py`:

```bash
python main.py
```

El script imprimirá el progreso en la consola, mostrando cada paso del flujo de trabajo. También generará una imagen del grafo (`research_assistant_mockup.png`) para visualizar su estructura.

## Requisitos

Asegúrese de tener Python instalado. Las dependencias se pueden instalar usando `pip`:

```bash
pip install -r requirements.txt
```

