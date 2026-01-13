"""
Interactive dashboard for Research Trends visualization.

Provides a Dash-based web interface for exploring research trends with:
- Publication timeline charts
- Author and institution rankings
- Keyword analysis and word clouds
- Network visualizations
- Geographic distribution maps
"""

from typing import Any, Dict, List, Optional
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    from dash import Dash, html, dcc, Input, Output, State
    import dash_bootstrap_components as dbc
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False

from research_trends.analyzer import TrendAnalyzer
from research_trends.recommender import Recommender
from research_trends.models import TrendData


class Dashboard:
    """Interactive dashboard for exploring research trends.
    
    Creates a web-based dashboard using Dash and Plotly for visualizing
    publication trends, author statistics, and research recommendations.
    
    Example:
        >>> dashboard = Dashboard(analyzer)
        >>> dashboard.run(port=8050)
    """
    
    def __init__(
        self,
        analyzer: TrendAnalyzer,
        title: str = "Research Trends Dashboard",
    ) -> None:
        """Initialize the dashboard.
        
        Args:
            analyzer: TrendAnalyzer instance with analyzed data.
            title: Dashboard title.
            
        Raises:
            ImportError: If Dash is not installed.
        """
        if not DASH_AVAILABLE:
            raise ImportError(
                "Dash is required for the dashboard. "
                "Install with: pip install research-trends-scopus[notebook]"
            )
        
        self.analyzer = analyzer
        self.trends = analyzer.analyze()
        self.recommender = Recommender(analyzer)
        self.title = title
        self.app: Optional[Dash] = None
    
    def create_app(self) -> Dash:
        """Create the Dash application.
        
        Returns:
            Configured Dash application.
        """
        app = Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            title=self.title,
        )
        
        app.layout = self._create_layout()
        self._setup_callbacks(app)
        
        self.app = app
        return app
    
    def _create_layout(self) -> dbc.Container:
        """Create the dashboard layout."""
        return dbc.Container([
            # Header
            dbc.Row([
                dbc.Col([
                    html.H1(self.title, className="text-center my-4"),
                    html.P(
                        f"Analyzing {len(self.analyzer.publications)} publications",
                        className="text-center text-muted"
                    ),
                ])
            ]),
            
            # Summary cards
            dbc.Row([
                dbc.Col(self._create_summary_card(
                    "Total Publications",
                    len(self.analyzer.publications),
                    "📚"
                ), md=3),
                dbc.Col(self._create_summary_card(
                    "Unique Authors",
                    len(self.trends.author_counts),
                    "👥"
                ), md=3),
                dbc.Col(self._create_summary_card(
                    "Total Citations",
                    self.trends.citation_stats.get('total', 0),
                    "📈"
                ), md=3),
                dbc.Col(self._create_summary_card(
                    "Open Access",
                    f"{self.trends.open_access_ratio:.1%}",
                    "🔓"
                ), md=3),
            ], className="mb-4"),
            
            # Tabs for different views
            dbc.Tabs([
                dbc.Tab(self._create_timeline_tab(), label="Timeline"),
                dbc.Tab(self._create_authors_tab(), label="Authors"),
                dbc.Tab(self._create_keywords_tab(), label="Keywords"),
                dbc.Tab(self._create_journals_tab(), label="Journals"),
                dbc.Tab(self._create_network_tab(), label="Network"),
                dbc.Tab(self._create_recommendations_tab(), label="Recommendations"),
            ], className="mb-4"),
            
            # Footer
            dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.P(
                        "Research Trends Dashboard | Powered by Scopus API",
                        className="text-center text-muted"
                    ),
                ])
            ]),
        ], fluid=True)
    
    def _create_summary_card(
        self,
        title: str,
        value: Any,
        icon: str,
    ) -> dbc.Card:
        """Create a summary statistics card."""
        return dbc.Card([
            dbc.CardBody([
                html.H2(icon, className="text-center"),
                html.H3(str(value), className="text-center"),
                html.P(title, className="text-center text-muted"),
            ])
        ], className="h-100")
    
    def _create_timeline_tab(self) -> dbc.Container:
        """Create the timeline visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("Publications Over Time"),
                    dcc.Graph(
                        id='timeline-chart',
                        figure=self._create_timeline_chart()
                    ),
                ], md=8),
                dbc.Col([
                    html.H4("Citation Trends"),
                    dcc.Graph(
                        id='citation-chart',
                        figure=self._create_citation_trend_chart()
                    ),
                ], md=4),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4("Growth Rate"),
                    dcc.Graph(
                        id='growth-chart',
                        figure=self._create_growth_chart()
                    ),
                ], md=6),
                dbc.Col([
                    html.H4("Document Types"),
                    dcc.Graph(
                        id='doctype-chart',
                        figure=self._create_document_type_chart()
                    ),
                ], md=6),
            ]),
        ], className="mt-4")
    
    def _create_authors_tab(self) -> dbc.Container:
        """Create the authors visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("Top Authors by Publication Count"),
                    dcc.Graph(
                        id='authors-chart',
                        figure=self._create_top_authors_chart()
                    ),
                ], md=6),
                dbc.Col([
                    html.H4("Top Affiliations"),
                    dcc.Graph(
                        id='affiliations-chart',
                        figure=self._create_top_affiliations_chart()
                    ),
                ], md=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4("Most Cited Publications"),
                    self._create_citations_table(),
                ])
            ], className="mt-4"),
        ], className="mt-4")
    
    def _create_keywords_tab(self) -> dbc.Container:
        """Create the keywords visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("Top Keywords"),
                    dcc.Graph(
                        id='keywords-chart',
                        figure=self._create_keywords_chart()
                    ),
                ], md=6),
                dbc.Col([
                    html.H4("Subject Areas"),
                    dcc.Graph(
                        id='subjects-chart',
                        figure=self._create_subject_areas_chart()
                    ),
                ], md=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4("Keyword Trends Over Time"),
                    dcc.Graph(
                        id='keyword-trends-chart',
                        figure=self._create_keyword_trends_chart()
                    ),
                ])
            ], className="mt-4"),
        ], className="mt-4")
    
    def _create_journals_tab(self) -> dbc.Container:
        """Create the journals visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("Top Journals/Conferences"),
                    dcc.Graph(
                        id='journals-chart',
                        figure=self._create_journals_chart()
                    ),
                ], md=8),
                dbc.Col([
                    html.H4("Open Access by Year"),
                    dcc.Graph(
                        id='oa-chart',
                        figure=self._create_open_access_chart()
                    ),
                ], md=4),
            ]),
        ], className="mt-4")
    
    def _create_network_tab(self) -> dbc.Container:
        """Create the network visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("Co-authorship Network"),
                    html.P(
                        "Network showing collaborations between authors. "
                        "Node size represents publication count, edge width "
                        "represents collaboration frequency.",
                        className="text-muted"
                    ),
                    dcc.Graph(
                        id='network-chart',
                        figure=self._create_network_chart(),
                        style={'height': '600px'}
                    ),
                ])
            ]),
        ], className="mt-4")
    
    def _create_recommendations_tab(self) -> dbc.Container:
        """Create the recommendations tab."""
        recommendations = self.recommender.get_recommendations(top_n=5)
        
        cards = []
        for rec in recommendations:
            color_map = {
                'emerging_topics': 'success',
                'research_gaps': 'warning',
                'collaborations': 'info',
                'venues': 'primary',
            }
            color = color_map.get(rec.category, 'secondary')
            
            cards.append(
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Badge(rec.category.replace('_', ' ').title(), color=color),
                        html.Span(f" Score: {rec.score:.2f}", className="float-end"),
                    ]),
                    dbc.CardBody([
                        html.H5(rec.title, className="card-title"),
                        html.P(rec.description, className="card-text"),
                        html.Small(rec.rationale, className="text-muted"),
                    ]),
                ], className="mb-3")
            )
        
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("Research Recommendations"),
                    html.P(
                        "AI-powered suggestions for research exploration based on "
                        "analysis of publication trends and patterns.",
                        className="text-muted mb-4"
                    ),
                    *cards,
                ])
            ]),
        ], className="mt-4")
    
    def _create_timeline_chart(self) -> go.Figure:
        """Create publications timeline chart."""
        yearly = self.trends.yearly_counts
        
        if not yearly:
            return go.Figure().add_annotation(text="No data available")
        
        df = pd.DataFrame({
            'Year': list(yearly.keys()),
            'Publications': list(yearly.values())
        }).sort_values('Year')
        
        fig = px.bar(
            df,
            x='Year',
            y='Publications',
            title='Publications per Year'
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Number of Publications',
            template='plotly_white'
        )
        
        return fig
    
    def _create_citation_trend_chart(self) -> go.Figure:
        """Create citation trends chart."""
        yearly_cites = self.trends.yearly_citations
        
        if not yearly_cites:
            return go.Figure().add_annotation(text="No data available")
        
        df = pd.DataFrame({
            'Year': list(yearly_cites.keys()),
            'Citations': list(yearly_cites.values())
        }).sort_values('Year')
        
        fig = px.line(
            df,
            x='Year',
            y='Citations',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Total Citations',
            template='plotly_white'
        )
        
        return fig
    
    def _create_growth_chart(self) -> go.Figure:
        """Create growth rate chart."""
        growth_rates = self.analyzer.get_growth_rate()
        
        if not growth_rates:
            return go.Figure().add_annotation(text="No data available")
        
        df = pd.DataFrame({
            'Year': list(growth_rates.keys()),
            'Growth Rate (%)': list(growth_rates.values())
        }).sort_values('Year')
        
        colors = ['green' if g > 0 else 'red' for g in df['Growth Rate (%)']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=df['Year'],
                y=df['Growth Rate (%)'],
                marker_color=colors
            )
        ])
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Growth Rate (%)',
            template='plotly_white'
        )
        
        return fig
    
    def _create_document_type_chart(self) -> go.Figure:
        """Create document type pie chart."""
        doc_types = self.trends.document_type_counts
        
        if not doc_types:
            return go.Figure().add_annotation(text="No data available")
        
        fig = px.pie(
            values=list(doc_types.values()),
            names=list(doc_types.keys()),
            hole=0.4
        )
        
        fig.update_layout(template='plotly_white')
        
        return fig
    
    def _create_top_authors_chart(self) -> go.Figure:
        """Create top authors bar chart."""
        top_authors = self.analyzer.get_top_authors(15)
        
        if not top_authors:
            return go.Figure().add_annotation(text="No data available")
        
        authors, counts = zip(*top_authors)
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(counts),
                y=list(authors),
                orientation='h'
            )
        ])
        
        fig.update_layout(
            xaxis_title='Publications',
            yaxis_title='Author',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def _create_top_affiliations_chart(self) -> go.Figure:
        """Create top affiliations bar chart."""
        top_affiliations = self.analyzer.get_top_affiliations(15)
        
        if not top_affiliations:
            return go.Figure().add_annotation(text="No data available")
        
        affiliations, counts = zip(*top_affiliations)
        # Truncate long names
        affiliations = [a[:40] + '...' if len(a) > 40 else a for a in affiliations]
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(counts),
                y=list(affiliations),
                orientation='h'
            )
        ])
        
        fig.update_layout(
            xaxis_title='Publications',
            yaxis_title='Affiliation',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def _create_citations_table(self) -> dbc.Table:
        """Create table of most cited publications."""
        most_cited = self.analyzer.get_most_cited(10)
        
        rows = []
        for i, pub in enumerate(most_cited, 1):
            title = pub.title[:80] + '...' if len(pub.title) > 80 else pub.title
            authors = ', '.join(pub.authors[:3])
            if len(pub.authors) > 3:
                authors += ' et al.'
            
            rows.append(html.Tr([
                html.Td(str(i)),
                html.Td(title),
                html.Td(authors),
                html.Td(str(pub.publication_year or 'N/A')),
                html.Td(str(pub.citation_count)),
            ]))
        
        return dbc.Table([
            html.Thead(html.Tr([
                html.Th('#'),
                html.Th('Title'),
                html.Th('Authors'),
                html.Th('Year'),
                html.Th('Citations'),
            ])),
            html.Tbody(rows)
        ], striped=True, hover=True, responsive=True)
    
    def _create_keywords_chart(self) -> go.Figure:
        """Create keywords bar chart."""
        top_keywords = self.analyzer.get_top_keywords(20)
        
        if not top_keywords:
            return go.Figure().add_annotation(text="No data available")
        
        keywords, counts = zip(*top_keywords)
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(counts),
                y=list(keywords),
                orientation='h'
            )
        ])
        
        fig.update_layout(
            xaxis_title='Frequency',
            yaxis_title='Keyword',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def _create_subject_areas_chart(self) -> go.Figure:
        """Create subject areas pie chart."""
        subject_areas = self.trends.subject_area_counts
        
        if not subject_areas:
            return go.Figure().add_annotation(text="No data available")
        
        # Get top 10
        sorted_areas = sorted(subject_areas.items(), key=lambda x: x[1], reverse=True)[:10]
        
        fig = px.pie(
            values=[v for _, v in sorted_areas],
            names=[k for k, _ in sorted_areas],
            hole=0.4
        )
        
        fig.update_layout(template='plotly_white')
        
        return fig
    
    def _create_keyword_trends_chart(self) -> go.Figure:
        """Create keyword trends over time chart."""
        keyword_df = self.analyzer.get_keyword_trends()
        
        if keyword_df.empty:
            return go.Figure().add_annotation(text="No data available")
        
        # Get top 5 keywords
        top_keywords = [kw for kw, _ in self.analyzer.get_top_keywords(5)]
        
        fig = go.Figure()
        
        for kw in top_keywords:
            if kw in keyword_df.columns:
                fig.add_trace(go.Scatter(
                    x=keyword_df.index,
                    y=keyword_df[kw],
                    mode='lines+markers',
                    name=kw
                ))
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Frequency',
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        
        return fig
    
    def _create_journals_chart(self) -> go.Figure:
        """Create journals bar chart."""
        top_journals = self.analyzer.get_top_journals(15)
        
        if not top_journals:
            return go.Figure().add_annotation(text="No data available")
        
        journals, counts = zip(*top_journals)
        journals = [j[:50] + '...' if len(j) > 50 else j for j in journals]
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(counts),
                y=list(journals),
                orientation='h'
            )
        ])
        
        fig.update_layout(
            xaxis_title='Publications',
            yaxis_title='Journal/Conference',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def _create_open_access_chart(self) -> go.Figure:
        """Create open access ratio chart."""
        oa_by_year = self.trends.yearly_open_access
        
        if not oa_by_year:
            return go.Figure().add_annotation(text="No data available")
        
        df = pd.DataFrame({
            'Year': list(oa_by_year.keys()),
            'Open Access Ratio': [v * 100 for v in oa_by_year.values()]
        }).sort_values('Year')
        
        fig = px.line(
            df,
            x='Year',
            y='Open Access Ratio',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Open Access (%)',
            template='plotly_white'
        )
        
        return fig
    
    def _create_network_chart(self) -> go.Figure:
        """Create co-authorship network visualization."""
        import networkx as nx
        
        network = self.analyzer.get_coauthorship_network()
        
        if not network.nodes or not network.edges:
            return go.Figure().add_annotation(text="No collaboration data available")
        
        # Build NetworkX graph
        G = nx.Graph()
        
        for node in network.nodes:
            G.add_node(node.id, weight=node.weight)
        
        for edge in network.edges:
            G.add_edge(edge.source, edge.target, weight=edge.weight)
        
        # Filter to top nodes for visibility
        if len(G.nodes) > 50:
            # Keep nodes with most connections
            degrees = dict(G.degree())
            top_nodes = sorted(degrees.keys(), key=lambda x: degrees[x], reverse=True)[:50]
            G = G.subgraph(top_nodes).copy()
        
        # Calculate layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Create edge traces
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node traces
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_size.append(min(30, 5 + G.degree(node) * 2))
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition='top center',
            textfont=dict(size=8),
            marker=dict(
                size=node_size,
                color='#1f77b4',
                line=dict(width=1, color='white')
            )
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                template='plotly_white'
            )
        )
        
        return fig
    
    def _setup_callbacks(self, app: Dash) -> None:
        """Setup Dash callbacks for interactivity."""
        # Add callbacks here for interactive features
        pass
    
    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 8050,
        debug: bool = False,
    ) -> None:
        """Run the dashboard server.
        
        Args:
            host: Host address to bind to.
            port: Port number.
            debug: Enable debug mode.
        """
        if self.app is None:
            self.create_app()
        
        print(f"Starting dashboard at http://{host}:{port}")
        self.app.run_server(host=host, port=port, debug=debug)
    
    def get_figures(self) -> Dict[str, go.Figure]:
        """Get all figures as a dictionary.
        
        Useful for embedding visualizations in notebooks or reports.
        
        Returns:
            Dictionary mapping figure names to Plotly figures.
        """
        return {
            'timeline': self._create_timeline_chart(),
            'citations': self._create_citation_trend_chart(),
            'growth': self._create_growth_chart(),
            'document_types': self._create_document_type_chart(),
            'top_authors': self._create_top_authors_chart(),
            'top_affiliations': self._create_top_affiliations_chart(),
            'keywords': self._create_keywords_chart(),
            'subject_areas': self._create_subject_areas_chart(),
            'keyword_trends': self._create_keyword_trends_chart(),
            'journals': self._create_journals_chart(),
            'open_access': self._create_open_access_chart(),
            'network': self._create_network_chart(),
        }
