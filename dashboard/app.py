"""
NREL SLOPE Geospatial Dashboard
Interactive dashboard for visualizing county energy data
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import sys
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_storage import DataStorage


class SLOPEDashboard:
    """Geospatial dashboard for NREL SLOPE county data"""

    def __init__(self, data_file=None):
        """
        Initialize dashboard

        Args:
            data_file (str): Path to data CSV file
        """
        self.storage = DataStorage()
        self.app = dash.Dash(__name__, title="NREL SLOPE County Dashboard")

        # Load data
        self.load_data(data_file)

        # Setup layout
        self.setup_layout()
        self.setup_callbacks()

    def load_data(self, data_file=None):
        """Load county data from storage"""
        if data_file:
            self.df = pd.read_csv(data_file)
        else:
            # Try to load most recent processed data
            processed_dir = Path("data/processed")
            csv_files = sorted(processed_dir.glob("counties_data_*.csv"), reverse=True)

            if csv_files:
                self.df = pd.read_csv(csv_files[0])
                print(f"Loaded data from: {csv_files[0]}")
            else:
                # Create sample data for demonstration
                self.df = self.create_sample_data()
                print("Using sample data")

    def create_sample_data(self):
        """Create sample data for demonstration"""
        import numpy as np

        # Create sample county data
        num_counties = 100
        state_fips = [f"{i:02d}" for i in range(1, 51)]

        data = {
            'geoid': [f"G{np.random.choice(state_fips)}{i:05d}" for i in range(num_counties)],
            'state_fips': np.random.choice(state_fips, num_counties),
            'county_fips': [f"{i:05d}" for i in range(num_counties)],
            'scrape_status': np.random.choice(['success', 'error'], num_counties, p=[0.9, 0.1]),
            'page_title': [f"County {i}" for i in range(num_counties)],
        }

        return pd.DataFrame(data)

    def setup_layout(self):
        """Setup dashboard layout"""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("NREL SLOPE County Energy Dashboard",
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
                html.P("Interactive visualization of county-level energy data from NREL SLOPE platform",
                      style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': 30}),
            ], style={'backgroundColor': '#ecf0f1', 'padding': '20px'}),

            # Stats Cards
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(str(len(self.df)), style={'margin': 0, 'color': '#3498db'}),
                        html.P("Total Counties", style={'margin': 0, 'color': '#7f8c8d'}),
                    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                             'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
                ], style={'flex': 1, 'margin': '10px'}),

                html.Div([
                    html.Div([
                        html.H3(str(len(self.df[self.df['scrape_status'] == 'success'])),
                               style={'margin': 0, 'color': '#2ecc71'}),
                        html.P("Successful Scrapes", style={'margin': 0, 'color': '#7f8c8d'}),
                    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                             'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
                ], style={'flex': 1, 'margin': '10px'}),

                html.Div([
                    html.Div([
                        html.H3(str(self.df['state_fips'].nunique()),
                               style={'margin': 0, 'color': '#e74c3c'}),
                        html.P("States Covered", style={'margin': 0, 'color': '#7f8c8d'}),
                    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white',
                             'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
                ], style={'flex': 1, 'margin': '10px'}),

            ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

            # Filters
            html.Div([
                html.Div([
                    html.Label("Filter by State FIPS:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='state-filter',
                        options=[{'label': 'All States', 'value': 'all'}] +
                                [{'label': f"State {s}", 'value': s}
                                 for s in sorted(self.df['state_fips'].unique())],
                        value='all',
                        style={'width': '100%'}
                    ),
                ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),

                html.Div([
                    html.Label("Filter by Status:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='status-filter',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'Success', 'value': 'success'},
                            {'label': 'Error', 'value': 'error'}
                        ],
                        value='all',
                        style={'width': '100%'}
                    ),
                ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
            ], style={'padding': '20px', 'backgroundColor': 'white', 'margin': '20px',
                     'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

            # Visualizations
            html.Div([
                # Distribution Chart
                html.Div([
                    dcc.Graph(id='distribution-chart'),
                ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),

                # Status Chart
                html.Div([
                    dcc.Graph(id='status-chart'),
                ], style={'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
            ]),

            # Data Table
            html.Div([
                html.H3("County Data", style={'color': '#2c3e50'}),
                html.Div(id='data-table'),
            ], style={'padding': '20px', 'backgroundColor': 'white', 'margin': '20px',
                     'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

            # Footer
            html.Div([
                html.P("Data Source: NREL SLOPE Platform",
                      style={'textAlign': 'center', 'color': '#95a5a6', 'margin': 0}),
                html.P("https://maps.nrel.gov/slope/",
                      style={'textAlign': 'center', 'color': '#95a5a6', 'margin': 0}),
            ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'marginTop': '40px'}),

        ], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f5f6fa'})

    def setup_callbacks(self):
        """Setup dashboard callbacks"""

        @self.app.callback(
            [Output('distribution-chart', 'figure'),
             Output('status-chart', 'figure'),
             Output('data-table', 'children')],
            [Input('state-filter', 'value'),
             Input('status-filter', 'value')]
        )
        def update_dashboard(state_value, status_value):
            # Filter data
            filtered_df = self.df.copy()

            if state_value != 'all':
                filtered_df = filtered_df[filtered_df['state_fips'] == state_value]

            if status_value != 'all':
                filtered_df = filtered_df[filtered_df['scrape_status'] == status_value]

            # Distribution chart
            state_counts = filtered_df['state_fips'].value_counts().reset_index()
            state_counts.columns = ['state_fips', 'count']

            dist_fig = px.bar(
                state_counts,
                x='state_fips',
                y='count',
                title='Counties by State FIPS',
                labels={'state_fips': 'State FIPS', 'count': 'Number of Counties'}
            )
            dist_fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Arial, sans-serif")
            )

            # Status chart
            status_counts = filtered_df['scrape_status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']

            status_fig = px.pie(
                status_counts,
                values='count',
                names='status',
                title='Scraping Status Distribution',
                color='status',
                color_discrete_map={'success': '#2ecc71', 'error': '#e74c3c'}
            )
            status_fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Arial, sans-serif")
            )

            # Data table
            table_data = filtered_df[['geoid', 'state_fips', 'county_fips',
                                      'scrape_status', 'page_title']].head(20)

            table = html.Table([
                html.Thead(
                    html.Tr([html.Th(col, style={'padding': '10px', 'backgroundColor': '#3498db',
                                                 'color': 'white', 'textAlign': 'left'})
                            for col in table_data.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(table_data.iloc[i][col],
                               style={'padding': '10px', 'borderBottom': '1px solid #ddd'})
                        for col in table_data.columns
                    ]) for i in range(len(table_data))
                ])
            ], style={'width': '100%', 'borderCollapse': 'collapse'})

            return dist_fig, status_fig, table

    def run(self, debug=True, port=8050):
        """
        Run the dashboard server

        Args:
            debug (bool): Run in debug mode
            port (int): Port number
        """
        print(f"\n{'='*60}")
        print("NREL SLOPE County Dashboard")
        print(f"{'='*60}")
        print(f"Starting server on http://localhost:{port}")
        print(f"Data loaded: {len(self.df)} counties")
        print(f"{'='*60}\n")

        self.app.run_server(debug=debug, port=port, host='0.0.0.0')


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="NREL SLOPE Geospatial Dashboard")
    parser.add_argument(
        "--data",
        help="Path to data CSV file"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Port number (default: 8050)"
    )
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode"
    )

    args = parser.parse_args()

    dashboard = SLOPEDashboard(data_file=args.data)
    dashboard.run(debug=not args.no_debug, port=args.port)


if __name__ == "__main__":
    main()
