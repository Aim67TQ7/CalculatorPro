import json
import plotly.graph_objects as go
import plotly.io as pio

class ChartService:
    def __init__(self):
        # Set default template for consistent styling
        pio.templates.default = "plotly_white"

    def fig_to_base64(self, fig: go.Figure) -> str:
        """Convert Plotly figure to JSON string for frontend rendering"""
        try:
            # Convert figure to JSON for frontend rendering
            return fig.to_json()
        except Exception as e:
            # Return empty string if conversion fails
            return ""

    def create_comparison_chart(self, x_data, y_data, x_title, y_title, title, highlight_x=None):
        """Create a generic comparison bar chart"""
        fig = go.Figure()

        # Add bar chart
        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            name='Values',
            marker_color='#1f77b4'
        ))

        # Highlight specific value if provided
        if highlight_x is not None and highlight_x in x_data:
            highlight_y = y_data[x_data.index(highlight_x)]
            fig.add_trace(go.Scatter(
                x=[highlight_x],
                y=[highlight_y],
                mode='markers',
                name='Selected',
                marker=dict(color='red', size=12)
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return fig

    def create_line_chart(self, x_data, y_data, x_title, y_title, title, line_name="Data"):
        """Create a generic line chart"""
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines+markers',
            name=line_name,
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))

        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return fig

    def create_multi_line_chart(self, data_series, x_title, y_title, title):
        """Create a multi-line chart for comparing multiple series"""
        fig = go.Figure()

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, (name, x_data, y_data) in enumerate(data_series):
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                name=name,
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6)
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return fig

    def create_scatter_plot(self, x_data, y_data, x_title, y_title, title, size_data=None):
        """Create a scatter plot with optional bubble sizing"""
        fig = go.Figure()

        marker_dict = dict(
            color='#1f77b4',
            opacity=0.7
        )
        
        if size_data:
            marker_dict['size'] = size_data
            marker_dict['sizemode'] = 'diameter'
            marker_dict['sizeref'] = max(size_data) / 50

        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='markers',
            name='Data Points',
            marker=marker_dict
        ))

        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return fig
