import json
import zlib
import base64
from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
from plotly.offline import plot
import html

class Renderer:
    """
    Main class for rendering individual self-contained HTML content with support for LaTeX, Plotly charts, and other features.
    Each instance renders a single piece of content (question or option).
    """
    
    def __init__(self, 
                 content: str,
                 need_latex: bool = False,
                 need_plotly: bool = False,
                 plotly_figure: Optional[go.Figure] = None,
                 plotly_config: Optional[Dict[str, Any]] = None,
                 custom_css: str = "",
                 custom_js: str = "",
                 title: str = "Content",
                 content_type: str = "general"):
        """
        Initialize renderer for a single piece of content.
        
        Args:
            content: The main content text
            need_latex: Whether to include KaTeX for LaTeX rendering
            need_plotly: Whether to include Plotly for interactive charts
            plotly_figure: Plotly figure object to render
            plotly_config: Plotly configuration options
            custom_css: Additional CSS styles
            custom_js: Additional JavaScript code
            title: HTML document title
            content_type: Type of content (question, option, general)
        """
        self.content = content
        self.need_latex = need_latex
        self.need_plotly = need_plotly
        self.plotly_figure = plotly_figure
        self.plotly_config = plotly_config or {}
        self.custom_css = custom_css
        self.custom_js = custom_js
        self.title = title
        self.content_type = content_type
        
        # Library versions
        self.katex_version = "0.16.8"
        self.plotly_version = "2.26.0"
        
    def render(self) -> str:
        """
        Render content into a self-contained HTML string.
        
        Returns:
            Self-contained HTML string ready for iframe rendering
        """
        html_parts = []
        
        # HTML document start
        html_parts.append(self._get_html_header())
        
        # CSS and external libraries
        html_parts.append(self._get_css_links())
        
        # Main content
        html_parts.append(self._get_body_content())
        
        # JavaScript libraries and scripts
        html_parts.append(self._get_js_scripts())
        
        # HTML document end
        html_parts.append(self._get_html_footer())
        
        return "\n".join(html_parts)
    
    def _get_html_header(self) -> str:
        """Generate HTML document header."""
        escaped_title = html.escape(self.title)
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escaped_title}</title>'''
    
    def _get_css_links(self) -> str:
        """Generate CSS links and styles."""
        css_parts = []
        
        # KaTeX CSS
        if self.need_latex:
            css_parts.append(f'''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{self.katex_version}/katex.min.css">''')
        
        # Compact styles optimized for embedding
        css_parts.append(f'''
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 8px;
            line-height: 1.4;
            color: #333;
            background-color: transparent;
            font-size: 14px;
        }}
        .content-container {{
            max-width: 100%;
            margin: 0;
            padding: 12px;
            background-color: white;
            border-radius: 6px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }}
        {self._get_content_type_styles()}
        .plotly-container {{
            margin: 8px 0;
            padding: 8px;
            background-color: #fafafa;
            border-radius: 4px;
            border: 1px solid #e8e8e8;
        }}
        .katex-display {{
            margin: 0.8em 0;
        }}
        .katex {{
            font-size: 1em;
        }}
        .content-text {{
            font-size: 14px;
            line-height: 1.5;
            margin: 0;
        }}
        .content-text h3 {{
            margin: 0 0 8px 0;
            font-size: 14px;
            font-weight: 600;
        }}
        .content-text p {{
            margin: 6px 0;
        }}
        .loading {{
            text-align: center;
            padding: 8px;
            color: #666;
            font-size: 10px;
        }}
        /* Ensure charts fit well in compact space */
        #plotly-div {{
            /* Maintain a 16:9 aspect ratio while remaining responsive */
            aspect-ratio: 16 / 9;
            width: 100%;
            min-height: 180px;
            height: auto !important;
        }}
        {self.custom_css}
    </style>''')
        
        css_parts.append('</head>')
        return "\n".join(css_parts)
    
    def _get_content_type_styles(self) -> str:
        """Get CSS styles based on content type."""
        if self.content_type == "question":
            return '''
        .content-container {
            border-left: 3px solid #007bff;
            background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        }
        .content-text {
            font-weight: 500;
            color: #2c3e50;
        }
        .content-container::before {
            content: "Q";
            display: inline-block;
            font-size: 10px;
            color: #007bff;
            font-weight: bold;
            background: #007bff;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            margin-bottom: 6px;
            margin-right: 6px;
        }'''
        elif self.content_type == "option":
            return '''
        .content-container {
            border-left: 3px solid #28a745;
            background: linear-gradient(135deg, #f8fff8 0%, #ffffff 100%);
        }
        .content-text {
            color: #2c3e50;
        }
        .content-container::before {
            content: "A";
            display: inline-block;
            font-size: 10px;
            color: white;
            font-weight: bold;
            background: #28a745;
            padding: 2px 6px;
            border-radius: 3px;
            margin-bottom: 6px;
            margin-right: 6px;
        }'''
        else:
            return '''
        .content-container {
            border-left: 3px solid #6c757d;
        }'''
    
    def _get_body_content(self) -> str:
        """Generate body content with plotly chart if needed."""
        body_parts = []
        body_parts.append('<body>')
        body_parts.append('    <div class="content-container">')
        body_parts.append('        <div class="content-text">')
        body_parts.append(f'            {self.content}')
        body_parts.append('        </div>')
        
        # Add plotly container if needed
        if self.need_plotly and self.plotly_figure:
            body_parts.append('        <div class="plotly-container">')
            body_parts.append('            <div id="plotly-div" class="loading">Loading chart...</div>')
            body_parts.append('        </div>')
        
        body_parts.append('    </div>')
        return "\n".join(body_parts)
    
    def _get_js_scripts(self) -> str:
        """Generate JavaScript scripts."""
        js_parts = []
        
        # KaTeX JavaScript
        if self.need_latex:
            js_parts.append(f'''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{self.katex_version}/katex.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{self.katex_version}/contrib/auto-render.min.js"></script>''')
        
        # Plotly JavaScript
        if self.need_plotly:
            js_parts.append(f'''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/{self.plotly_version}/plotly.min.js"></script>''')
        
        # Main JavaScript
        js_parts.append('''
    <script>
        document.addEventListener("DOMContentLoaded", function() {''')
        
        # KaTeX rendering
        if self.need_latex:
            js_parts.append('''
            renderMathInElement(document.body, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false,
                errorColor: "#cc0000"
            });''')
        
        # Plotly rendering
        if self.need_plotly and self.plotly_figure:
            js_parts.append(self._generate_plotly_js())
        
        # Custom JavaScript
        if self.custom_js:
            js_parts.append(f'''
            {self.custom_js}''')
        
        js_parts.append('''
        });
    </script>''')
        
        return "\n".join(js_parts)
    
    def _generate_plotly_js(self) -> str:
        """Generate Plotly JavaScript for rendering the figure."""
        if not self.plotly_figure:
            return ""
        
        try:
            # Convert plotly figure to JSON with proper escaping
            fig_dict = self.plotly_figure.to_dict()
            fig_json = json.dumps(fig_dict, separators=(',', ':'))
            
            # Compact plotly config optimized for small embedded charts
            default_config = {
                'displayModeBar': False,  # Hide toolbar for compact display
                'responsive': True,
                'staticPlot': False,
                'doubleClick': False,
                'showTips': False,
                'showAxisDragHandles': False,
                'showAxisRangeEntryBoxes': False,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'resetScale2d', 'zoomIn2d', 'zoomOut2d']
            }
            
            # Merge with custom config
            config = {**default_config, **self.plotly_config}
            config_json = json.dumps(config, separators=(',', ':'))
            
            return f'''
            try {{
                const plotlyData = {fig_json};
                const plotlyConfig = {config_json};
                
                if (plotlyData.layout) {{
                    plotlyData.layout.margin = plotlyData.layout.margin || {{}};
                    Object.assign(plotlyData.layout.margin, {{l: 40, r: 20, t: 30, b: 40}});
                    plotlyData.layout.height = 200;
                    plotlyData.layout.font = plotlyData.layout.font || {{}};
                    plotlyData.layout.font.size = 11;
                    if (plotlyData.layout.showlegend !== false) {{
                        plotlyData.layout.legend = plotlyData.layout.legend || {{}};
                        Object.assign(plotlyData.layout.legend, {{
                            font: {{size: 10}},
                            orientation: "h",
                            y: -0.2
                        }});
                    }}
                }}
                
                Plotly.newPlot("plotly-div", plotlyData.data, plotlyData.layout, plotlyConfig);
                
                window.addEventListener("resize", function() {{
                    if (typeof Plotly !== "undefined" && Plotly.Plots) {{
                        Plotly.Plots.resize("plotly-div");
                    }}
                }});
            }} catch (error) {{
                console.error("Error rendering Plotly chart:", error);
                const plotlyDiv = document.getElementById("plotly-div");
                if (plotlyDiv) {{
                    plotlyDiv.innerHTML = "<div style=\\"text-align:center;padding:20px;color:#666;font-size:12px;\\">Chart unavailable</div>";
                }}
            }}'''
        except Exception as e:
            error_msg = str(e).replace('"', '\\"')
            return f'''
            console.error("Error preparing Plotly chart:", "{error_msg}");
            const plotlyDiv = document.getElementById("plotly-div");
            if (plotlyDiv) {{
                plotlyDiv.innerHTML = "<div style=\\"text-align:center;padding:20px;color:#666;font-size:12px;\\">Chart generation failed</div>";
            }}'''
    
    def _get_html_footer(self) -> str:
        """Generate HTML document footer."""
        return '''</body>
</html>'''


class HTMLRenderer:
    """
    Main class for rendering a full HTML document from multiple content blocks.
    This class orchestrates multiple Renderer instances to build a complete page.
    """
    
    def __init__(self, title: str = "Rendered HTML", custom_css: str = "", custom_js: str = ""):
        """
        Initialize the HTML renderer.
        
        Args:
            title: The title of the HTML document.
            custom_css: Custom CSS to be included in the document.
            custom_js: Custom JavaScript to be included in the document.
        """
        self.title = title
        self.custom_css = custom_css
        self.custom_js = custom_js
        self.content_blocks: List[Dict[str, Any]] = []
        
        # Library versions
        self.katex_version = "0.16.8"
        self.plotly_version = "2.26.0"
        
    def add_content(self, content: str, content_type: str = "general"):
        """
        Add a text content block.
        
        Args:
            content: The text content to add.
            content_type: The type of content (e.g., 'question', 'option').
        """
        self.content_blocks.append({
            "type": "text",
            "content": content,
            "content_type": content_type
        })
        return self
        
    def add_plotly_figure(self, fig: go.Figure, config: Optional[Dict[str, Any]] = None):
        """
        Add a Plotly figure to the document.
        
        Args:
            fig: The Plotly figure object.
            config: Optional Plotly configuration.
        """
        self.content_blocks.append({
            "type": "plotly",
            "figure": fig,
            "config": config or {"responsive": True}
        })
        return self

    def add_table(self, data: List[List[Any]], headers: Optional[List[str]] = None):
        """Add a table block to the document."""
        self.content_blocks.append({
            "type": "table",
            "data": data,
            "headers": headers or []
        })
        return self

    def render_as_blocks(self) -> List[str]:
        """Render every content block as its own self-contained HTML string."""
        rendered: List[str] = []
        for idx, block in enumerate(self.content_blocks):
            try:
                if block["type"] == "text":
                    r = Renderer(
                        content=block["content"],
                        need_latex=True,
                        content_type=block.get("content_type", "general"),
                        title=f"{self.title} – Text {idx+1}"
                    )
                    rendered.append(r.render())
                elif block["type"] == "plotly":
                    r = Renderer(
                        content="",
                        need_plotly=True,
                        plotly_figure=block["figure"],
                        plotly_config=block["config"],
                        title=f"{self.title} – Chart {idx+1}"
                    )
                    rendered.append(r.render())
                elif block["type"] == "table":
                    table_html = self.generate_table_html(block)
                    r = Renderer(content=table_html, title=f"{self.title} – Table {idx+1}")
                    rendered.append(r.render())
            except Exception as e:
                # Create an error block if rendering fails
                error_r = Renderer(
                    content=f'<div style="color: red; padding: 10px; border: 1px solid red; border-radius: 4px;">Error rendering block {idx+1}: {html.escape(str(e))}</div>',
                    title=f"{self.title} – Error {idx+1}"
                )
                rendered.append(error_r.render())
        return rendered

    def render(self, compact: bool = False) -> str:
        """Render the full HTML document.
        
        Args:
            compact: If True, removes extra whitespace for a smaller output.
        """
        html_content = self._render_full_html()
        if compact:
            import re
            # Remove all extra whitespace and newlines
            html_content = re.sub(r'\s+', ' ', html_content).strip()
        return html_content
        
    def render_as_json(self, compact: bool = False) -> str:
        """Render the HTML and return as a JSON string.
        
        Args:
            compact: If True, removes extra whitespace from the HTML.
        """
        html_content = self.render(compact=compact)
        # Use a custom JSON encoder to avoid escaping issues
        return json.dumps({"html": html_content}, ensure_ascii=False, separators=(',', ':'))
        
    def render_as_compressed_json(self) -> str:
        """Render as minified HTML and compress with zlib + base64."""
        html_content = self.render(compact=True)
        compressed = zlib.compress(html_content.encode('utf-8'))
        return json.dumps({
            "html_compressed": base64.b64encode(compressed).decode('ascii')
        }, ensure_ascii=False, separators=(',', ':'))
        
    def _render_full_html(self) -> str:
        """Internal: Generate the full HTML document."""
        # Determine if LaTeX or Plotly are needed
        need_latex = any(block.get("type") == "text" for block in self.content_blocks)
        need_plotly = any(block.get("type") == "plotly" for block in self.content_blocks)
        
        # Start HTML document
        escaped_title = html.escape(self.title)
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escaped_title}</title>
    {self._get_css(need_latex)}
</head>
<body>
    <div class="main-container">
'''
        
        # Render each content block
        for i, block in enumerate(self.content_blocks):
            try:
                if block["type"] == "text":
                    html_content += self._render_text_block(block)
                elif block["type"] == "plotly":
                    html_content += self._render_plotly_block(block, i)
                elif block["type"] == "table":
                    html_content += self.generate_table_html(block)
            except Exception as e:
                # Add error block if rendering fails
                error_html = f'''<div style="color: red; padding: 10px; border: 1px solid red; border-radius: 4px; margin: 10px 0;">
                    Error rendering block {i+1}: {html.escape(str(e))}
                </div>'''
                html_content += error_html
        
        # End HTML document
        html_content += f'''
    </div>
    {self._get_js(need_latex, need_plotly)}
</body>
</html>'''
        
        return html_content
    
    def _render_text_block(self, block: Dict[str, Any]) -> str:
        """Render a single text block."""
        renderer = Renderer(
            content=block["content"],
            content_type=block["content_type"],
            need_latex=True
        )
        # Extract just the body content for embedding
        body_content = renderer._get_body_content()
        # Remove body tags
        body_content = body_content.replace("<body>", "").replace("</body>", "").strip()
        return body_content

    def generate_table_html(self, block: Dict[str, Any]) -> str:
        """Generate HTML for a single table block."""
        headers = block["headers"]
        data = block["data"]

        html_content = '<div class="table-container">'
        html_content += '<table>'

        if headers:
            html_content += '<thead><tr>'
            for header in headers:
                html_content += f'<th>{html.escape(str(header))}</th>'
            html_content += '</tr></thead>'

        html_content += '<tbody>'
        for row in data:
            html_content += '<tr>'
            for cell in row:
                html_content += f'<td>{html.escape(str(cell))}</td>'
            html_content += '</tr>'
        html_content += '</tbody>'

        html_content += '</table>'
        html_content += '</div>'
        return html_content

    def _render_plotly_block(self, block: Dict[str, Any], block_id: int) -> str:
        """Render a placeholder container for a Plotly figure."""
        div_id = f"plotly-div-{block_id}"
        container = f'''
        <div class="plotly-container">
            <div id="{div_id}" class="loading">Loading chart...</div>
        </div>'''
        return container
    
    def _get_css(self, need_latex: bool) -> str:
        """Generate CSS for the full document."""
        css = ""
        if need_latex:
            css += f'''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{self.katex_version}/katex.min.css">'''
        
        css += f'''
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 16px;
            background-color: #f4f4f9;
            color: #333;
        }}
        .main-container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .content-container {{
            margin-bottom: 16px;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }}
        .plotly-container {{
            margin: 16px 0;
            padding: 12px;
            background-color: #fafafa;
            border-radius: 4px;
            border: 1px solid #e8e8e8;
        }}
        .table-container {{
            margin: 16px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .loading {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }}
        .plotly-div {{
            aspect-ratio: 16 / 9;
            width: 100%;
            min-height: 240px;
            height: auto !important;
        }}
        {self.custom_css}
    </style>'''
        return css
    
    def _get_js(self, need_latex: bool, need_plotly: bool) -> str:
        """Generate JS for the full document."""
        js = ""
        if need_latex:
            js += f'''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{self.katex_version}/katex.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{self.katex_version}/contrib/auto-render.min.js"></script>'''
        
        if need_plotly:
            js += f'''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/{self.plotly_version}/plotly.min.js"></script>'''
            
        js += '''
    <script>
        document.addEventListener("DOMContentLoaded", function() {'''
        
        if need_latex:
            js += '''
            if (typeof renderMathInElement !== "undefined") {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "$", right: "$", display: false},
                        {left: "\\(", right: "\\)", display: false},
                        {left: "\\[", right: "\\]", display: true}
                    ],
                    throwOnError: false
                });
            }'''
            
        if need_plotly:
            js += self._get_all_plotly_js()
            
        if self.custom_js:
            js += f'''
            {self.custom_js}'''
            
        js += '''
        });
    </script>'''
        return js
    
    def _get_all_plotly_js(self) -> str:
        """Generate JS for all Plotly charts."""
        js = ""
        for i, block in enumerate(self.content_blocks):
            if block["type"] == "plotly":
                try:
                    fig = block["figure"]
                    config = block["config"]
                    div_id = f"plotly-div-{i}"
                    
                    # Convert figure to dict and then to JSON with proper escaping
                    fig_dict = fig.to_dict()
                    fig_json = json.dumps(fig_dict, separators=(',', ':'))
                    
                    default_config = {
                        'displayModeBar': True,
                        'responsive': True,
                    }
                    final_config = {**default_config, **config}
                    config_json = json.dumps(final_config, separators=(',', ':'))
                    
                    js += f'''
                try {{
                    if (typeof Plotly !== "undefined") {{
                        const plotlyData_{i} = {fig_json};
                        const plotlyConfig_{i} = {config_json};
                        Plotly.newPlot("{div_id}", plotlyData_{i}.data, plotlyData_{i}.layout, plotlyConfig_{i});
                    }} else {{
                        console.error("Plotly library not loaded");
                        document.getElementById("{div_id}").innerHTML = "<div style=\\"text-align:center;padding:20px;color:#666;font-size:12px;\\">Plotly library not available</div>";
                    }}
                }} catch (e) {{
                    console.error("Error rendering plotly chart {i}:", e);
                    document.getElementById("{div_id}").innerHTML = "<div style=\\"text-align:center;padding:20px;color:#666;font-size:12px;\\">Error rendering chart</div>";
                }}'''
                except Exception as e:
                    error_msg = str(e).replace('"', '\\"')
                    js += f'''
                console.error("Error preparing chart {i}:", "{error_msg}");
                document.getElementById("plotly-div-{i}").innerHTML = "<div style=\\"text-align:center;padding:20px;color:#666;font-size:12px;\\">Chart preparation failed</div>";'''
        
        # Add resize handlers
        js += '''
        window.addEventListener("resize", function() {
            if (typeof Plotly !== "undefined" && Plotly.Plots) {'''
        
        for i, block in enumerate(self.content_blocks):
            if block["type"] == "plotly":
                div_id = f"plotly-div-{i}"
                js += f'''
                try {{
                    Plotly.Plots.resize("{div_id}");
                }} catch (e) {{
                    console.warn("Error resizing chart {i}:", e);
                }}'''
        
        js += '''
            }
        });'''
        
        return js
