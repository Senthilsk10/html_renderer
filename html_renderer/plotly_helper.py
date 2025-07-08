
import plotly.graph_objects as go
from typing import List, Union

# Plotly Helper Functions
class PlotlyHelper:
    """Helper class for creating common Plotly visualizations."""
    
    @staticmethod
    def create_bar_chart(x_data: List[str], y_data: List[float], 
                        title: str = "", x_label: str = "", y_label: str = "",
                        color: str = "#3498db") -> go.Figure:
        """Create a compact bar chart optimized for embedding."""
        fig = go.Figure(data=[
            go.Bar(x=x_data, y=y_data, marker_color=color)
        ])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14)) if title else None,
            xaxis=dict(title=x_label, tickfont=dict(size=10)),
            yaxis=dict(title=y_label, tickfont=dict(size=10)),
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=40),
            height=200
        )
        return fig
    
    @staticmethod
    def create_line_chart(x_data: List[Union[str, float]], y_data: List[float],
                         title: str = "", x_label: str = "", y_label: str = "",
                         color: str = "#e74c3c") -> go.Figure:
        """Create a compact line chart optimized for embedding."""
        fig = go.Figure(data=[
            go.Scatter(x=x_data, y=y_data, mode='lines+markers', 
                      line=dict(color=color, width=2),
                      marker=dict(size=4, color=color))
        ])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14)) if title else None,
            xaxis=dict(title=x_label, tickfont=dict(size=10)),
            yaxis=dict(title=y_label, tickfont=dict(size=10)),
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=40),
            height=200
        )
        return fig
    
    @staticmethod
    def create_pie_chart(labels: List[str], values: List[float],
                        title: str = "") -> go.Figure:
        """Create a compact pie chart optimized for embedding."""
        fig = go.Figure(data=[
            go.Pie(labels=labels, values=values, hole=0.3, textfont=dict(size=10))
        ])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14)) if title else None,
            template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20),
            height=200,
            showlegend=True,
            legend=dict(font=dict(size=9), orientation="h", y=-0.1)
        )
        return fig
    
    @staticmethod
    def create_scatter_plot(x_data: List[float], y_data: List[float],
                           title: str = "", x_label: str = "", y_label: str = "",
                           color: str = "#9b59b6") -> go.Figure:
        """Create a compact scatter plot optimized for embedding."""
        fig = go.Figure(data=[
            go.Scatter(x=x_data, y=y_data, mode='markers',
                      marker=dict(size=6, color=color, opacity=0.7))
        ])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14)) if title else None,
            xaxis=dict(title=x_label, tickfont=dict(size=10)),
            yaxis=dict(title=y_label, tickfont=dict(size=10)),
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=40),
            height=200
        )
        return fig
    
    @staticmethod
    def create_histogram(data: List[float], title: str = "", 
                        x_label: str = "", bins: int = 15) -> go.Figure:
        """Create a compact histogram optimized for embedding."""
        fig = go.Figure(data=[
            go.Histogram(x=data, nbinsx=bins, marker_color="#f39c12")
        ])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14)) if title else None,
            xaxis=dict(title=x_label, tickfont=dict(size=10)),
            yaxis=dict(title="Frequency", tickfont=dict(size=10)),
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=40),
            height=200
        )
        return fig
    
    @staticmethod
    def create_box_plot(data: List[float], title: str = "",
                       y_label: str = "") -> go.Figure:
        """Create a compact box plot optimized for embedding."""
        fig = go.Figure(data=[
            go.Box(y=data, marker_color="#1abc9c", name="")
        ])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14)) if title else None,
            yaxis=dict(title=y_label, tickfont=dict(size=10)),
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=40),
            height=200,
            showlegend=False
        )
        return fig
    
    @staticmethod
    def create_heatmap(z_data: List[List[float]], x_labels: List[str], 
                      y_labels: List[str], title: str = "") -> go.Figure:
        """Create a compact heatmap optimized for embedding."""
        fig = go.Figure(data=[
            go.Heatmap(z=z_data, x=x_labels, y=y_labels, colorscale='Viridis')
        ])
        fig.update_layout(
            title=dict(text=title, font=dict(size=14)) if title else None,
            template="plotly_white",
            margin=dict(l=60, r=20, t=40, b=40),
            height=200,
            xaxis=dict(tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=9))
        )
        return fig
