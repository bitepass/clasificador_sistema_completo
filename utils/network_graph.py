"""
Utilidad de Grafos de Red para OSINT-Nexus
Genera visualizaciones de relaciones entre entidades descubiertas
"""
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import json

class NetworkGraphGenerator:
    """Generador de grafos de red para visualizar relaciones OSINT"""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.node_colors = {
            "domain": "#1f77b4",
            "email": "#ff7f0e", 
            "username": "#2ca02c",
            "ip": "#d62728",
            "person": "#9467bd",
            "organization": "#8c564b",
            "location": "#e377c2",
            "technology": "#7f7f7f",
            "breach": "#bcbd22",
            "social_profile": "#17becf"
        }
        
        self.edge_colors = {
            "owns": "#ff0000",
            "uses": "#00ff00",
            "located_at": "#0000ff",
            "works_for": "#ffff00",
            "related_to": "#ff00ff",
            "exposed_in": "#00ffff",
            "found_on": "#ff8800"
        }
    
    def add_domain_data(self, domain_data: Dict[str, Any]) -> None:
        """Añade datos de dominio al grafo"""
        try:
            domain = domain_data.get("domain_info", {}).get("domain", "unknown")
            
            # Nodo del dominio
            self.graph.add_node(domain, type="domain", label=domain)
            
            # Subdominios
            for subdomain in domain_data.get("subdomains", []):
                subdomain_name = subdomain.get("name", "")
                if subdomain_name:
                    self.graph.add_node(subdomain_name, type="domain", label=subdomain_name)
                    self.graph.add_edge(domain, subdomain_name, type="owns")
            
            # IPs
            for ip_info in domain_data.get("ip_addresses", []):
                ip = ip_info.get("value", "")
                if ip:
                    self.graph.add_node(ip, type="ip", label=ip)
                    self.graph.add_edge(domain, ip, type="uses")
            
            # Tecnologías
            for tech in domain_data.get("technologies", []):
                tech_name = tech.get("name", "")
                if tech_name:
                    self.graph.add_node(tech_name, type="technology", label=tech_name)
                    self.graph.add_edge(domain, tech_name, type="uses")
            
            # Vulnerabilidades
            for vuln in domain_data.get("vulnerabilities", []):
                vuln_name = vuln.get("cve", "")
                if vuln_name:
                    self.graph.add_node(vuln_name, type="vulnerability", label=vuln_name)
                    self.graph.add_edge(domain, vuln_name, type="exposed_in")
                    
        except Exception as e:
            print(f"Error añadiendo datos de dominio: {str(e)}")
    
    def add_email_data(self, email_data: Dict[str, Any]) -> None:
        """Añade datos de email al grafo"""
        try:
            email = email_data.get("email_info", {}).get("email", "unknown")
            username = email_data.get("email_info", {}).get("username", "")
            domain = email_data.get("email_info", {}).get("domain", "")
            
            # Nodo del email
            self.graph.add_node(email, type="email", label=email)
            
            # Nodo de la persona
            if username:
                self.graph.add_node(username, type="person", label=username)
                self.graph.add_edge(email, username, type="owned_by")
            
            # Nodo del dominio
            if domain:
                self.graph.add_node(domain, type="domain", label=domain)
                self.graph.add_edge(email, domain, type="uses")
            
            # Emails relacionados
            for related_email in email_data.get("related_emails", []):
                related_addr = related_email.get("email", "")
                if related_addr:
                    self.graph.add_node(related_addr, type="email", label=related_addr)
                    self.graph.add_edge(email, related_addr, type="related_to")
                    
                    # Información de la persona
                    first_name = related_email.get("first_name", "")
                    last_name = related_email.get("last_name", "")
                    if first_name or last_name:
                        person_name = f"{first_name} {last_name}".strip()
                        self.graph.add_node(person_name, type="person", label=person_name)
                        self.graph.add_edge(related_addr, person_name, type="owned_by")
            
            # Brechas de datos
            for breach in email_data.get("breaches", []):
                breach_name = breach.get("name", "")
                if breach_name:
                    self.graph.add_node(breach_name, type="breach", label=breach_name)
                    self.graph.add_edge(email, breach_name, type="exposed_in")
                    
        except Exception as e:
            print(f"Error añadiendo datos de email: {str(e)}")
    
    def add_username_data(self, username_data: Dict[str, Any]) -> None:
        """Añade datos de nombre de usuario al grafo"""
        try:
            username = username_data.get("username", "unknown")
            
            # Nodo de la persona
            self.graph.add_node(username, type="person", label=username)
            
            # Perfiles sociales encontrados
            for profile in username_data.get("profiles", []):
                platform = profile.get("platform", "")
                profile_url = profile.get("url", "")
                
                if profile.get("exists") and profile_url:
                    profile_node = f"{platform}_{username}"
                    self.graph.add_node(profile_node, type="social_profile", label=f"{platform}: {username}")
                    self.graph.add_edge(username, profile_node, type="found_on")
                    
        except Exception as e:
            print(f"Error añadiendo datos de username: {str(e)}")
    
    def add_social_data(self, social_data: Dict[str, Any]) -> None:
        """Añade datos de redes sociales al grafo"""
        try:
            profile_info = social_data.get("profile_info", {})
            platform = profile_info.get("platform", "")
            username = profile_info.get("username", "")
            
            if platform and username:
                profile_node = f"{platform}_{username}"
                self.graph.add_node(profile_node, type="social_profile", label=f"{platform}: {username}")
                
                # Nodo de la persona
                self.graph.add_node(username, type="person", label=username)
                self.graph.add_edge(username, profile_node, type="owns")
                
                # Conexiones (si están disponibles)
                for connection in social_data.get("connections", []):
                    connection_name = connection.get("name", "")
                    if connection_name:
                        self.graph.add_node(connection_name, type="person", label=connection_name)
                        self.graph.add_edge(profile_node, connection_name, type="connected_to")
                        
        except Exception as e:
            print(f"Error añadiendo datos sociales: {str(e)}")
    
    def generate_plotly_graph(self, layout: str = "spring") -> go.Figure:
        """Genera un grafo interactivo usando Plotly"""
        try:
            # Calcular posiciones de los nodos
            if layout == "spring":
                pos = nx.spring_layout(self.graph, k=1, iterations=50)
            elif layout == "circular":
                pos = nx.circular_layout(self.graph)
            elif layout == "random":
                pos = nx.random_layout(self.graph)
            else:
                pos = nx.spring_layout(self.graph)
            
            # Preparar datos para Plotly
            edge_x = []
            edge_y = []
            edge_colors = []
            edge_text = []
            
            for edge in self.graph.edges(data=True):
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                
                edge_type = edge[2].get("type", "related_to")
                edge_colors.extend([self.edge_colors.get(edge_type, "#cccccc")] * 3)
                edge_text.extend([edge_type] * 3)
            
            # Crear trazas de edges
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.5, color=edge_colors),
                hoverinfo='text',
                text=edge_text,
                mode='lines',
                showlegend=False
            )
            
            # Preparar datos de nodos
            node_x = []
            node_y = []
            node_text = []
            node_colors = []
            node_sizes = []
            
            for node in self.graph.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                
                node_data = self.graph.nodes[node]
                node_type = node_data.get("type", "unknown")
                node_label = node_data.get("label", str(node))
                
                node_text.append(f"{node_label}<br>Type: {node_type}")
                node_colors.append(self.node_colors.get(node_type, "#cccccc"))
                
                # Tamaño basado en el tipo
                if node_type == "domain":
                    node_sizes.append(20)
                elif node_type == "person":
                    node_sizes.append(15)
                else:
                    node_sizes.append(10)
            
            # Crear traza de nodos
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=[node.split('<br>')[0] for node in node_text],
                textposition="bottom center",
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    line=dict(width=2, color='white')
                ),
                showlegend=False
            )
            
            # Crear figura
            fig = go.Figure(data=[edge_trace, node_trace],
                          layout=go.Layout(
                              title='OSINT Network Graph',
                              titlefont_size=16,
                              showlegend=False,
                              hovermode='closest',
                              margin=dict(b=20,l=5,r=5,t=40),
                              annotations=[ dict(
                                  text="Hover over nodes for details",
                                  showarrow=False,
                                  xref="paper", yref="paper",
                                  x=0.005, y=-0.002 ) ],
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                          )
            
            return fig
            
        except Exception as e:
            print(f"Error generando grafo Plotly: {str(e)}")
            return go.Figure()
    
    def generate_statistics(self) -> Dict[str, Any]:
        """Genera estadísticas del grafo"""
        try:
            stats = {
                "total_nodes": self.graph.number_of_nodes(),
                "total_edges": self.graph.number_of_edges(),
                "node_types": {},
                "edge_types": {},
                "density": nx.density(self.graph),
                "connected_components": nx.number_connected_components(self.graph),
                "average_clustering": nx.average_clustering(self.graph),
                "average_shortest_path": None
            }
            
            # Contar tipos de nodos
            for node, data in self.graph.nodes(data=True):
                node_type = data.get("type", "unknown")
                stats["node_types"][node_type] = stats["node_types"].get(node_type, 0) + 1
            
            # Contar tipos de edges
            for edge in self.graph.edges(data=True):
                edge_type = edge[2].get("type", "unknown")
                stats["edge_types"][edge_type] = stats["edge_types"].get(edge_type, 0) + 1
            
            # Calcular camino más corto promedio (solo si el grafo es conexo)
            if nx.is_connected(self.graph):
                try:
                    stats["average_shortest_path"] = nx.average_shortest_path_length(self.graph)
                except:
                    pass
            
            return stats
            
        except Exception as e:
            print(f"Error generando estadísticas: {str(e)}")
            return {}
    
    def export_graph(self, format: str = "json") -> str:
        """Exporta el grafo en diferentes formatos"""
        try:
            if format.lower() == "json":
                # Convertir a formato JSON serializable
                graph_data = {
                    "nodes": [],
                    "edges": []
                }
                
                for node, data in self.graph.nodes(data=True):
                    graph_data["nodes"].append({
                        "id": str(node),
                        "type": data.get("type", "unknown"),
                        "label": data.get("label", str(node))
                    })
                
                for edge in self.graph.edges(data=True):
                    graph_data["edges"].append({
                        "source": str(edge[0]),
                        "target": str(edge[1]),
                        "type": edge[2].get("type", "related_to")
                    })
                
                return json.dumps(graph_data, indent=2)
            
            elif format.lower() == "gexf":
                # Formato GEXF para Gephi
                return nx.write_gexf(self.graph, "network_graph.gexf")
            
            elif format.lower() == "graphml":
                # Formato GraphML
                return nx.write_graphml(self.graph, "network_graph.graphml")
            
            else:
                raise ValueError(f"Formato no soportado: {format}")
                
        except Exception as e:
            print(f"Error exportando grafo: {str(e)}")
            return ""
    
    def clear_graph(self) -> None:
        """Limpia el grafo"""
        self.graph.clear()
    
    def get_central_nodes(self, top_k: int = 10) -> List[tuple]:
        """Obtiene los nodos más centrales del grafo"""
        try:
            centrality = nx.degree_centrality(self.graph)
            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            return sorted_nodes[:top_k]
        except Exception as e:
            print(f"Error calculando centralidad: {str(e)}")
            return []