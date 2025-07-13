from __future__ import annotations

from typing import Dict, Any, Tuple

import networkx as nx
import matplotlib.pyplot as plt


def build_graph_from_results(target: str, results: Dict[str, Any]) -> Tuple[nx.Graph, plt.Figure]:
    """Construye un grafo simple conectando el objetivo con cada entidad encontrada.

    Debido a que cada módulo devuelve estructuras diferentes, este builder aplica
    reglas heurísticas:
    * Si el valor es un str -> crea nodo y lo conecta al target.
    * Si es una lista -> cada elemento es nodo.
    * Si es un dict -> toma claves y/o valores según profundidad simple.

    Parameters
    ----------
    target : str
        El valor del objetivo buscado.
    results : Dict[str, Any]
        Diccionario de resultados devuelto por el módulo.

    Returns
    -------
    Tuple[nx.Graph, plt.Figure]
        El grafo y su figura para mostrar.
    """
    G = nx.Graph()
    G.add_node(target, type="target")

    def _add_edge(entity):
        if not entity or entity == target:
            return
        G.add_node(entity)
        G.add_edge(target, entity)

    for section, content in results.items():
        if isinstance(content, str):
            _add_edge(f"{section}: {content[:30]}")
        elif isinstance(content, list):
            for item in content:
                _add_edge(f"{section}: {str(item)[:30]}")
        elif isinstance(content, dict):
            for k, v in content.items():
                if isinstance(v, (str, int, float)):
                    _add_edge(f"{k}: {str(v)[:30]}")
                elif isinstance(v, list):
                    for item in v:
                        _add_edge(f"{k}: {str(item)[:30]}")
        else:
            _add_edge(str(content))

    # Dibujamos
    pos = nx.spring_layout(G, seed=7, k=0.5)  # reproducible
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="#90caf9", ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif", ax=ax)
    ax.set_axis_off()
    fig.tight_layout()
    return G, fig