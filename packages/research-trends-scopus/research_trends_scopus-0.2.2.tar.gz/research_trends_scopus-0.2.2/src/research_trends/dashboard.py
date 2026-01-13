"""
Interactive dashboard for Research Trends visualization.

Provides a Dash-based web interface for exploring research trends with:
- Key findings summary with AI insights
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

# Fixed chart height for consistency
CHART_HEIGHT = 350
CHART_HEIGHT_SMALL = 280
CHART_HEIGHT_LARGE = 400


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
        self._key_findings = self._generate_key_findings()
    
    def _generate_key_findings(self) -> List[Dict[str, Any]]:
        """Generate key findings from the analysis."""
        findings = []
        
        # Publication trend finding
        yearly = self.trends.yearly_counts
        if yearly:
            years = sorted(yearly.keys())
            if len(years) >= 2:
                recent_year = years[-1]
                prev_year = years[-2]
                growth = ((yearly[recent_year] - yearly[prev_year]) / yearly[prev_year] * 100) if yearly[prev_year] > 0 else 0
                trend_direction = "📈 Growing" if growth > 0 else "📉 Declining"
                findings.append({
                    "icon": "📊",
                    "title": "Publication Trend",
                    "value": f"{abs(growth):.1f}%",
                    "description": f"{trend_direction} from {prev_year} to {recent_year}",
                    "color": "success" if growth > 0 else "danger"
                })
        
        # Top contributor
        top_authors = self.analyzer.get_top_authors(1)
        if top_authors:
            author, count = top_authors[0]
            findings.append({
                "icon": "🏆",
                "title": "Top Contributor",
                "value": author[:25] + "..." if len(author) > 25 else author,
                "description": f"{count} publications",
                "color": "primary"
            })
        
        # Most impactful publication
        most_cited = self.analyzer.get_most_cited(1)
        if most_cited:
            pub = most_cited[0]
            findings.append({
                "icon": "⭐",
                "title": "Highest Impact",
                "value": f"{pub.citation_count:,} citations",
                "description": pub.title[:50] + "..." if len(pub.title) > 50 else pub.title,
                "color": "warning"
            })
        
        # Hot topic
        top_keywords = self.analyzer.get_top_keywords(1)
        if top_keywords:
            keyword, count = top_keywords[0]
            findings.append({
                "icon": "🔥",
                "title": "Trending Topic",
                "value": keyword,
                "description": f"Appears in {count} publications",
                "color": "info"
            })
        
        # Research output
        total_pubs = len(self.analyzer.publications)
        total_citations = self.trends.citation_stats.get('total', 0)
        avg_citations = total_citations / total_pubs if total_pubs > 0 else 0
        findings.append({
            "icon": "📚",
            "title": "Avg. Impact",
            "value": f"{avg_citations:.1f}",
            "description": "citations per publication",
            "color": "secondary"
        })
        
        return findings
    
    def create_app(self) -> Dash:
        """Create the Dash application.
        
        Returns:
            Configured Dash application.
        """
        app = Dash(
            __name__,
            external_stylesheets=[
                dbc.themes.FLATLY,
                "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css"
            ],
            title=self.title,
            suppress_callback_exceptions=True,
        )
        
        # Custom CSS for modern styling
        app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --card-shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            }
            body {
                background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
                min-height: 100vh;
            }
            .dashboard-header {
                background: var(--primary-gradient);
                color: white;
                padding: 2rem 0;
                margin-bottom: 2rem;
                box-shadow: var(--card-shadow);
            }
            .stat-card {
                background: white;
                border-radius: 12px;
                padding: 1.25rem;
                box-shadow: var(--card-shadow);
                transition: all 0.3s ease;
                border: none;
                height: 100%;
            }
            .stat-card:hover {
                transform: translateY(-4px);
                box-shadow: var(--card-shadow-hover);
            }
            .finding-card {
                background: white;
                border-radius: 12px;
                padding: 1rem;
                box-shadow: var(--card-shadow);
                transition: all 0.3s ease;
                border-left: 4px solid;
                height: 100%;
            }
            .finding-card:hover {
                transform: translateY(-2px);
                box-shadow: var(--card-shadow-hover);
            }
            .chart-container {
                background: white;
                border-radius: 12px;
                padding: 1rem;
                box-shadow: var(--card-shadow);
                margin-bottom: 1.5rem;
                overflow: hidden;
            }
            .chart-title {
                font-size: 1rem;
                font-weight: 600;
                color: #374151;
                margin-bottom: 0.75rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #e5e7eb;
            }
            .nav-tabs .nav-link {
                border: none;
                color: #6b7280;
                font-weight: 500;
                padding: 0.75rem 1.5rem;
                border-radius: 8px 8px 0 0;
                transition: all 0.2s ease;
            }
            .nav-tabs .nav-link:hover {
                color: #374151;
                background: #f3f4f6;
            }
            .nav-tabs .nav-link.active {
                color: #667eea;
                background: white;
                border-bottom: 3px solid #667eea;
            }
            .tab-content {
                background: transparent;
                padding: 1.5rem 0;
            }
            .recommendation-card {
                background: white;
                border-radius: 12px;
                box-shadow: var(--card-shadow);
                margin-bottom: 1rem;
                overflow: hidden;
                transition: all 0.3s ease;
            }
            .recommendation-card:hover {
                box-shadow: var(--card-shadow-hover);
            }
            .table-container {
                max-height: 400px;
                overflow-y: auto;
            }
            .badge-category {
                font-size: 0.75rem;
                padding: 0.35rem 0.75rem;
                border-radius: 20px;
            }
            @media (max-width: 768px) {
                .stat-card, .finding-card {
                    margin-bottom: 1rem;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
        
        app.layout = self._create_layout()
        self._setup_callbacks(app)
        
        self.app = app
        return app
    
    def _create_layout(self) -> html.Div:
        """Create the dashboard layout."""
        return html.Div([
            # Header
            html.Div([
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            html.H1(self.title, className="mb-2", style={"fontWeight": "700"}),
                            html.P(
                                f"📊 Analyzing {len(self.analyzer.publications):,} publications",
                                className="mb-0 opacity-75"
                            ),
                        ], className="text-center")
                    ])
                ], fluid=True)
            ], className="dashboard-header"),
            
            dbc.Container([
                # Key Findings Section
                html.Div([
                    html.H4([
                        html.I(className="bi bi-lightbulb me-2"),
                        "Key Findings"
                    ], className="mb-3", style={"color": "#374151", "fontWeight": "600"}),
                    dbc.Row([
                        dbc.Col(
                            self._create_finding_card(finding),
                            xs=12, sm=6, md=4, lg=2, className="mb-3"
                        ) for finding in self._key_findings[:6]
                    ]),
                ], className="mb-4"),
                
                # Summary Statistics
                dbc.Row([
                    dbc.Col(self._create_stat_card(
                        "Total Publications",
                        f"{len(self.analyzer.publications):,}",
                        "bi-journal-text",
                        "#667eea"
                    ), xs=6, md=3, className="mb-3"),
                    dbc.Col(self._create_stat_card(
                        "Unique Authors",
                        f"{len(self.trends.author_counts):,}",
                        "bi-people",
                        "#10b981"
                    ), xs=6, md=3, className="mb-3"),
                    dbc.Col(self._create_stat_card(
                        "Total Citations",
                        f"{self.trends.citation_stats.get('total', 0):,}",
                        "bi-graph-up-arrow",
                        "#f59e0b"
                    ), xs=6, md=3, className="mb-3"),
                    dbc.Col(self._create_stat_card(
                        "Open Access",
                        f"{self.trends.open_access_ratio:.1%}",
                        "bi-unlock",
                        "#06b6d4"
                    ), xs=6, md=3, className="mb-3"),
                ], className="mb-4"),
                
                # Tabs for different views
                dbc.Tabs([
                    dbc.Tab(self._create_overview_tab(), label="Overview", tab_id="overview"),
                    dbc.Tab(self._create_timeline_tab(), label="Timeline", tab_id="timeline"),
                    dbc.Tab(self._create_authors_tab(), label="Authors", tab_id="authors"),
                    dbc.Tab(self._create_keywords_tab(), label="Keywords", tab_id="keywords"),
                    dbc.Tab(self._create_journals_tab(), label="Venues", tab_id="journals"),
                    dbc.Tab(self._create_network_tab(), label="Network", tab_id="network"),
                    dbc.Tab(self._create_recommendations_tab(), label="Insights", tab_id="recommendations"),
                ], id="main-tabs", active_tab="overview", className="mb-0"),
                
                # Footer
                html.Div([
                    html.Hr(className="my-4"),
                    html.P([
                        "Research Trends Dashboard v0.2.1 | ",
                        html.A("Powered by Multiple Academic APIs", href="#", className="text-muted")
                    ], className="text-center text-muted small"),
                ], className="mt-4 pb-4"),
            ], fluid=True),
        ])
    
    def _create_stat_card(
        self,
        title: str,
        value: str,
        icon: str,
        color: str,
    ) -> html.Div:
        """Create a modern stat card."""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className=f"bi {icon}", style={"fontSize": "1.5rem", "color": color})
                    ], style={
                        "width": "48px",
                        "height": "48px",
                        "borderRadius": "10px",
                        "background": f"{color}15",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    })
                ], width="auto"),
                dbc.Col([
                    html.P(title, className="mb-0 text-muted small"),
                    html.H4(value, className="mb-0", style={"fontWeight": "700", "color": "#1f2937"}),
                ]),
            ], align="center", className="g-3")
        ], className="stat-card")
    
    def _create_finding_card(self, finding: Dict[str, Any]) -> html.Div:
        """Create a key finding card."""
        color_map = {
            "success": "#10b981",
            "primary": "#667eea",
            "warning": "#f59e0b",
            "info": "#06b6d4",
            "danger": "#ef4444",
            "secondary": "#6b7280"
        }
        border_color = color_map.get(finding.get("color", "secondary"), "#6b7280")
        
        return html.Div([
            html.Div(finding["icon"], style={"fontSize": "1.5rem", "marginBottom": "0.5rem"}),
            html.P(finding["title"], className="text-muted small mb-1", style={"fontSize": "0.75rem"}),
            html.H6(finding["value"], className="mb-1", style={"fontWeight": "600", "color": "#1f2937"}),
            html.Small(finding["description"], className="text-muted", style={"fontSize": "0.7rem"}),
        ], className="finding-card", style={"borderLeftColor": border_color})
    
    def _create_overview_tab(self) -> dbc.Container:
        """Create the overview tab with main visualizations."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Publications Over Time", className="chart-title"),
                        dcc.Graph(
                            id='overview-timeline',
                            figure=self._create_timeline_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT}px'}
                        ),
                    ], className="chart-container")
                ], md=8),
                dbc.Col([
                    html.Div([
                        html.H6("Document Types", className="chart-title"),
                        dcc.Graph(
                            id='overview-doctype',
                            figure=self._create_document_type_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT}px'}
                        ),
                    ], className="chart-container")
                ], md=4),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Top 10 Authors", className="chart-title"),
                        dcc.Graph(
                            id='overview-authors',
                            figure=self._create_top_authors_chart(10),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
                dbc.Col([
                    html.Div([
                        html.H6("Top 10 Keywords", className="chart-title"),
                        dcc.Graph(
                            id='overview-keywords',
                            figure=self._create_keywords_chart(10),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
            ]),
        ], fluid=True, className="px-0 pt-3")
    
    def _create_timeline_tab(self) -> dbc.Container:
        """Create the timeline visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Publication Timeline", className="chart-title"),
                        dcc.Graph(
                            id='timeline-chart',
                            figure=self._create_timeline_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT}px'}
                        ),
                    ], className="chart-container")
                ], md=8),
                dbc.Col([
                    html.Div([
                        html.H6("Citation Trends", className="chart-title"),
                        dcc.Graph(
                            id='citation-chart',
                            figure=self._create_citation_trend_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT}px'}
                        ),
                    ], className="chart-container")
                ], md=4),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Year-over-Year Growth", className="chart-title"),
                        dcc.Graph(
                            id='growth-chart',
                            figure=self._create_growth_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_SMALL}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
                dbc.Col([
                    html.Div([
                        html.H6("Document Types Distribution", className="chart-title"),
                        dcc.Graph(
                            id='doctype-chart',
                            figure=self._create_document_type_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_SMALL}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
            ]),
        ], fluid=True, className="px-0 pt-3")
    
    def _create_authors_tab(self) -> dbc.Container:
        """Create the authors visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Top Authors by Publications", className="chart-title"),
                        dcc.Graph(
                            id='authors-chart',
                            figure=self._create_top_authors_chart(15),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_LARGE}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
                dbc.Col([
                    html.Div([
                        html.H6("Top Institutions", className="chart-title"),
                        dcc.Graph(
                            id='affiliations-chart',
                            figure=self._create_top_affiliations_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_LARGE}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Most Cited Publications", className="chart-title"),
                        html.Div(
                            self._create_citations_table(),
                            className="table-container"
                        ),
                    ], className="chart-container")
                ])
            ]),
        ], fluid=True, className="px-0 pt-3")
    
    def _create_keywords_tab(self) -> dbc.Container:
        """Create the keywords visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Top Keywords", className="chart-title"),
                        dcc.Graph(
                            id='keywords-chart',
                            figure=self._create_keywords_chart(20),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_LARGE}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
                dbc.Col([
                    html.Div([
                        html.H6("Subject Areas", className="chart-title"),
                        dcc.Graph(
                            id='subjects-chart',
                            figure=self._create_subject_areas_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_LARGE}px'}
                        ),
                    ], className="chart-container")
                ], md=6),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Keyword Trends Over Time", className="chart-title"),
                        dcc.Graph(
                            id='keyword-trends-chart',
                            figure=self._create_keyword_trends_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT}px'}
                        ),
                    ], className="chart-container")
                ])
            ]),
        ], fluid=True, className="px-0 pt-3")
    
    def _create_journals_tab(self) -> dbc.Container:
        """Create the journals visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Top Venues (Journals & Conferences)", className="chart-title"),
                        dcc.Graph(
                            id='journals-chart',
                            figure=self._create_journals_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_LARGE}px'}
                        ),
                    ], className="chart-container")
                ], md=8),
                dbc.Col([
                    html.Div([
                        html.H6("Open Access Trend", className="chart-title"),
                        dcc.Graph(
                            id='oa-chart',
                            figure=self._create_open_access_chart(),
                            config={'displayModeBar': False},
                            style={'height': f'{CHART_HEIGHT_LARGE}px'}
                        ),
                    ], className="chart-container")
                ], md=4),
            ]),
        ], fluid=True, className="px-0 pt-3")
    
    def _create_network_tab(self) -> dbc.Container:
        """Create the network visualization tab."""
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Co-authorship Network", className="chart-title"),
                        html.P(
                            "Node size = publication count • Edge width = collaboration frequency",
                            className="text-muted small mb-2"
                        ),
                        dcc.Graph(
                            id='network-chart',
                            figure=self._create_network_chart(),
                            config={'displayModeBar': True, 'scrollZoom': True},
                            style={'height': '500px'}
                        ),
                    ], className="chart-container")
                ])
            ]),
        ], fluid=True, className="px-0 pt-3")
    
    def _create_recommendations_tab(self) -> dbc.Container:
        """Create the recommendations tab."""
        recommendations = self.recommender.get_recommendations(top_n=6)
        
        cards = []
        color_map = {
            'emerging_topics': ('#10b981', 'bi-lightning-charge'),
            'research_gaps': ('#f59e0b', 'bi-search'),
            'collaborations': ('#06b6d4', 'bi-people'),
            'venues': ('#667eea', 'bi-journal-bookmark'),
        }
        
        for rec in recommendations:
            color, icon = color_map.get(rec.category, ('#6b7280', 'bi-lightbulb'))
            
            cards.append(
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className=f"bi {icon} me-2"),
                                html.Span(
                                    rec.category.replace('_', ' ').title(),
                                    className="badge-category",
                                    style={"background": f"{color}20", "color": color}
                                ),
                            ], className="d-flex align-items-center mb-2"),
                            html.Div(
                                f"{rec.score:.0%}",
                                className="small text-muted"
                            ),
                        ], className="d-flex justify-content-between align-items-start"),
                        html.H6(rec.title, className="mb-2", style={"fontWeight": "600"}),
                        html.P(rec.description, className="small text-muted mb-2"),
                        html.Small(rec.rationale, className="text-muted", style={"fontSize": "0.75rem"}),
                    ], className="recommendation-card p-3")
                ], md=6, lg=4, className="mb-3")
            )
        
        return dbc.Container([
            html.Div([
                html.H6([
                    html.I(className="bi bi-stars me-2"),
                    "AI-Powered Research Insights"
                ], className="mb-1", style={"fontWeight": "600"}),
                html.P(
                    "Actionable recommendations based on publication pattern analysis",
                    className="text-muted small mb-4"
                ),
            ]),
            dbc.Row(cards),
        ], fluid=True, className="px-0 pt-3")
    
    def _create_timeline_chart(self) -> go.Figure:
        """Create publications timeline chart."""
        yearly = self.trends.yearly_counts
        
        if not yearly:
            return self._empty_figure("No timeline data available")
        
        df = pd.DataFrame({
            'Year': list(yearly.keys()),
            'Publications': list(yearly.values())
        }).sort_values('Year')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Year'],
            y=df['Publications'],
            marker_color='#667eea',
            marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>%{y} publications<extra></extra>'
        ))
        
        # Add trend line
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Publications'],
            mode='lines',
            line=dict(color='#764ba2', width=2, dash='dot'),
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Publications',
            template='plotly_white',
            showlegend=False,
            margin=dict(l=40, r=20, t=20, b=40),
            xaxis=dict(tickmode='linear', dtick=1),
            bargap=0.3,
        )
        
        return fig
    
    def _empty_figure(self, message: str) -> go.Figure:
        """Create an empty figure with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="#6b7280")
        )
        fig.update_layout(
            template='plotly_white',
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        )
        return fig
        
    def _create_citation_trend_chart(self) -> go.Figure:
        """Create citation trends chart."""
        yearly_cites = self.trends.yearly_citations
        
        if not yearly_cites:
            return self._empty_figure("No citation data available")
        
        df = pd.DataFrame({
            'Year': list(yearly_cites.keys()),
            'Citations': list(yearly_cites.values())
        }).sort_values('Year')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Citations'],
            mode='lines+markers',
            line=dict(color='#10b981', width=2),
            marker=dict(size=8, color='#10b981'),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)',
            hovertemplate='<b>%{x}</b><br>%{y:,} citations<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Citations',
            template='plotly_white',
            margin=dict(l=40, r=20, t=20, b=40),
        )
        
        return fig
    
    def _create_growth_chart(self) -> go.Figure:
        """Create growth rate chart."""
        growth_rates = self.analyzer.get_growth_rate()
        
        if not growth_rates:
            return self._empty_figure("No growth data available")
        
        df = pd.DataFrame({
            'Year': list(growth_rates.keys()),
            'Growth Rate (%)': list(growth_rates.values())
        }).sort_values('Year')
        
        colors = ['#10b981' if g > 0 else '#ef4444' for g in df['Growth Rate (%)']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Year'],
            y=df['Growth Rate (%)'],
            marker_color=colors,
            marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>%{y:.1f}% growth<extra></extra>'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="#9ca3af", line_width=1)
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Growth %',
            template='plotly_white',
            margin=dict(l=40, r=20, t=20, b=40),
            bargap=0.3,
        )
        
        return fig
    
    def _create_document_type_chart(self) -> go.Figure:
        """Create document type pie chart."""
        doc_types = self.trends.document_type_counts
        
        if not doc_types:
            return self._empty_figure("No document type data")
        
        # Sort and take top 6
        sorted_types = sorted(doc_types.items(), key=lambda x: x[1], reverse=True)[:6]
        
        colors = ['#667eea', '#764ba2', '#10b981', '#f59e0b', '#06b6d4', '#ef4444']
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            values=[v for _, v in sorted_types],
            labels=[k for k, _ in sorted_types],
            hole=0.5,
            marker=dict(colors=colors[:len(sorted_types)]),
            textposition='outside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>%{value} (%{percent})<extra></extra>'
        ))
        
        fig.update_layout(
            template='plotly_white',
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
        )
        
        return fig
    
    def _create_top_authors_chart(self, n: int = 15) -> go.Figure:
        """Create top authors bar chart."""
        top_authors = self.analyzer.get_top_authors(n)
        
        if not top_authors:
            return self._empty_figure("No author data available")
        
        authors, counts = zip(*top_authors)
        authors = [a[:30] + '...' if len(a) > 30 else a for a in authors]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(counts),
            y=list(authors),
            orientation='h',
            marker_color='#667eea',
            marker_line_width=0,
            hovertemplate='<b>%{y}</b><br>%{x} publications<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title='Publications',
            yaxis_title='',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=10, r=20, t=20, b=40),
            bargap=0.2,
        )
        
        return fig
    
    def _create_top_affiliations_chart(self) -> go.Figure:
        """Create top affiliations bar chart."""
        top_affiliations = self.analyzer.get_top_affiliations(15)
        
        if not top_affiliations:
            return self._empty_figure("No affiliation data available")
        
        affiliations, counts = zip(*top_affiliations)
        affiliations = [a[:35] + '...' if len(a) > 35 else a for a in affiliations]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(counts),
            y=list(affiliations),
            orientation='h',
            marker_color='#10b981',
            marker_line_width=0,
            hovertemplate='<b>%{y}</b><br>%{x} publications<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title='Publications',
            yaxis_title='',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=10, r=20, t=20, b=40),
            bargap=0.2,
        )
        
        return fig
    
    def _create_citations_table(self) -> dbc.Table:
        """Create table of most cited publications."""
        most_cited = self.analyzer.get_most_cited(10)
        
        rows = []
        for i, pub in enumerate(most_cited, 1):
            title = pub.title[:60] + '...' if len(pub.title) > 60 else pub.title
            authors = ', '.join(pub.authors[:2])
            if len(pub.authors) > 2:
                authors += ' et al.'
            
            rows.append(html.Tr([
                html.Td(str(i), style={"fontWeight": "600", "color": "#667eea"}),
                html.Td(title, style={"fontSize": "0.85rem"}),
                html.Td(authors, className="text-muted", style={"fontSize": "0.8rem"}),
                html.Td(str(pub.publication_year or 'N/A'), className="text-center"),
                html.Td(
                    html.Span(f"{pub.citation_count:,}", className="badge bg-warning text-dark"),
                    className="text-center"
                ),
            ]))
        
        return dbc.Table([
            html.Thead(html.Tr([
                html.Th('#', style={"width": "40px"}),
                html.Th('Title'),
                html.Th('Authors', style={"width": "150px"}),
                html.Th('Year', style={"width": "60px"}, className="text-center"),
                html.Th('Citations', style={"width": "80px"}, className="text-center"),
            ]), className="table-light"),
            html.Tbody(rows)
        ], striped=True, hover=True, responsive=True, size="sm", className="mb-0")
    
    def _create_keywords_chart(self, n: int = 20) -> go.Figure:
        """Create keywords bar chart."""
        top_keywords = self.analyzer.get_top_keywords(n)
        
        if not top_keywords:
            return self._empty_figure("No keyword data available")
        
        keywords, counts = zip(*top_keywords)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(counts),
            y=list(keywords),
            orientation='h',
            marker_color='#f59e0b',
            marker_line_width=0,
            hovertemplate='<b>%{y}</b><br>%{x} occurrences<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title='Frequency',
            yaxis_title='',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=10, r=20, t=20, b=40),
            bargap=0.2,
        )
        
        return fig
    
    def _create_subject_areas_chart(self) -> go.Figure:
        """Create subject areas pie chart."""
        subject_areas = self.trends.subject_area_counts
        
        if not subject_areas:
            return self._empty_figure("No subject area data")
        
        sorted_areas = sorted(subject_areas.items(), key=lambda x: x[1], reverse=True)[:8]
        
        colors = ['#667eea', '#764ba2', '#10b981', '#f59e0b', '#06b6d4', '#ef4444', '#8b5cf6', '#ec4899']
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            values=[v for _, v in sorted_areas],
            labels=[k[:25] + '...' if len(k) > 25 else k for k, _ in sorted_areas],
            hole=0.5,
            marker=dict(colors=colors[:len(sorted_areas)]),
            textposition='outside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>%{value} (%{percent})<extra></extra>'
        ))
        
        fig.update_layout(
            template='plotly_white',
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
        )
        
        return fig
    
    def _create_keyword_trends_chart(self) -> go.Figure:
        """Create keyword trends over time chart."""
        keyword_df = self.analyzer.get_keyword_trends()
        
        if keyword_df.empty:
            return self._empty_figure("No keyword trend data")
        
        top_keywords = [kw for kw, _ in self.analyzer.get_top_keywords(5)]
        
        colors = ['#667eea', '#10b981', '#f59e0b', '#06b6d4', '#ef4444']
        
        fig = go.Figure()
        
        for i, kw in enumerate(top_keywords):
            if kw in keyword_df.columns:
                fig.add_trace(go.Scatter(
                    x=keyword_df.index,
                    y=keyword_df[kw],
                    mode='lines+markers',
                    name=kw[:20] + '...' if len(kw) > 20 else kw,
                    line=dict(color=colors[i % len(colors)], width=2),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{kw}</b><br>Year: %{{x}}<br>Count: %{{y}}<extra></extra>'
                ))
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Frequency',
            template='plotly_white',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5,
                font=dict(size=10)
            ),
            margin=dict(l=40, r=20, t=40, b=40),
        )
        
        return fig
    
    def _create_journals_chart(self) -> go.Figure:
        """Create journals bar chart."""
        top_journals = self.analyzer.get_top_journals(15)
        
        if not top_journals:
            return self._empty_figure("No venue data available")
        
        journals, counts = zip(*top_journals)
        journals = [j[:45] + '...' if len(j) > 45 else j for j in journals]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(counts),
            y=list(journals),
            orientation='h',
            marker_color='#06b6d4',
            marker_line_width=0,
            hovertemplate='<b>%{y}</b><br>%{x} publications<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title='Publications',
            yaxis_title='',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=10, r=20, t=20, b=40),
            bargap=0.2,
        )
        
        return fig
    
    def _create_open_access_chart(self) -> go.Figure:
        """Create open access ratio chart."""
        oa_by_year = self.trends.yearly_open_access
        
        if not oa_by_year:
            return self._empty_figure("No open access data")
        
        df = pd.DataFrame({
            'Year': list(oa_by_year.keys()),
            'Open Access Ratio': [v * 100 for v in oa_by_year.values()]
        }).sort_values('Year')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Open Access Ratio'],
            mode='lines+markers',
            line=dict(color='#8b5cf6', width=2),
            marker=dict(size=8, color='#8b5cf6'),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.1)',
            hovertemplate='<b>%{x}</b><br>%{y:.1f}% Open Access<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='OA %',
            template='plotly_white',
            margin=dict(l=40, r=20, t=20, b=40),
            yaxis=dict(range=[0, 100]),
        )
        
        return fig
    
    def _create_network_chart(self) -> go.Figure:
        """Create co-authorship network visualization."""
        import networkx as nx
        
        network = self.analyzer.get_coauthorship_network()
        
        if not network.nodes or not network.edges:
            return self._empty_figure("No collaboration data available")
        
        G = nx.Graph()
        
        for node in network.nodes:
            G.add_node(node.id, weight=node.weight)
        
        for edge in network.edges:
            G.add_edge(edge.source, edge.target, weight=edge.weight)
        
        # Filter to top nodes for visibility
        if len(G.nodes) > 40:
            degrees = dict(G.degree())
            top_nodes = sorted(degrees.keys(), key=lambda x: degrees[x], reverse=True)[:40]
            G = G.subgraph(top_nodes).copy()
        
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
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
            line=dict(width=0.8, color='rgba(150, 150, 150, 0.5)'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node traces
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            degree = G.degree(node)
            node_text.append(f"{node}<br>{degree} collaborations")
            node_size.append(min(40, 8 + degree * 3))
            node_color.append(degree)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale='Viridis',
                line=dict(width=1, color='white'),
                showscale=True,
                colorbar=dict(
                    title="Connections",
                    thickness=15,
                    len=0.5,
                    x=1.02
                )
            )
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                template='plotly_white',
                margin=dict(l=20, r=20, t=20, b=20),
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
        self.app.run(host=host, port=port, debug=debug)
    
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
