# HTML Renderer Package

A lightweight utility for generating **self-contained HTML snippets** for educational content such as questions, options, tables, and interactive Plotly charts. Each HTML string can be directly embedded in an `<iframe>` on the front-end, ensuring strict isolation between blocks.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Renderer Class](#renderer-class)
- [HTMLRenderer Class](#htmlrenderer-class)
- [PlotlyHelper](#plotlyhelper)
- [Output Formats](#output-formats)
- [Examples](#examples)
- [Best Practices](#best-practices)

## Installation

```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
from html_renderer.renderer import HTMLRenderer, Renderer
from html_renderer.plotly_helper import PlotlyHelper

# Single block rendering
renderer = Renderer(
    content="<p>Hello, World!</p>",
    need_latex=False,
    content_type="general"
)
single_html = renderer.render()

# Multiple blocks with HTMLRenderer
multi_renderer = (
    HTMLRenderer(title="Math Quiz")
    .add_content("<h2>Question 1</h2><p>What is 2+2?</p>", content_type="question")
    .add_plotly_figure(PlotlyHelper.create_bar_chart(["A", "B", "C"], [10, 20, 15]))
    .add_table([[1, "Correct"], [2, "Incorrect"]], ["ID", "Answer"])
)

# Get different output formats
full_html = multi_renderer.render()  # Single HTML document
blocks = multi_renderer.render_as_blocks()  # List of HTML strings
json_output = multi_renderer.render_as_json()  # JSON string
compressed = multi_renderer.render_as_compressed_json()  # Compressed JSON
```

## Renderer Class

Renders a single block of content into a self-contained HTML document.

### Initialization
```python
renderer = Renderer(
    content: str,                    # HTML content to render
    need_latex: bool = False,        # Enable LaTeX support
    need_plotly: bool = False,       # Enable Plotly support
    plotly_figure: Optional[go.Figure] = None,  # Plotly figure to include
    plotly_config: Optional[Dict] = None,      # Custom Plotly config
    title: str = "Rendered Content", # Page title
    content_type: str = "general"    # Type of content (affects styling)
)
```

### Methods
- `render(compact: bool = False) -> str`: Renders the content to HTML
  - `compact`: If True, removes extra whitespace for smaller output

## HTMLRenderer Class

Manages multiple content blocks and provides various output formats.

### Initialization
```python
renderer = HTMLRenderer(
    title: str = "Rendered Content",  # Document title
    custom_css: Optional[str] = None,  # Additional CSS
    custom_js: Optional[str] = None    # Additional JavaScript
)
```

### Core Methods
- `add_content(content: str, content_type: str = "general") -> HTMLRenderer`
  - Adds text/HTML content
  - `content_type`: "question", "option", or "general"

- `add_plotly_figure(figure: go.Figure, config: Optional[Dict] = None) -> HTMLRenderer`
  - Adds an interactive Plotly chart
  - `config`: Custom Plotly configuration

- `add_table(data: List[List[Any]], headers: Optional[List[str]] = None) -> HTMLRenderer`
  - Renders a data table
  - `data`: 2D list of table cells
  - `headers`: Optional column headers

### Output Methods
- `render(compact: bool = False) -> str`
  - Returns a single HTML document with all blocks

- `render_as_blocks() -> List[str]`
  - Returns a list of HTML strings, one per block

- `render_as_json(compact: bool = False) -> str`
  - Returns JSON string with format: `{"html": "<div>...</div>"}`

- `render_as_compressed_json() -> str`
  - Returns compressed and base64-encoded HTML
  - Format: `{"html_compressed": "eJx9kM1OwzAMhF9l5BQ5OYUe+gM9cYQKqVXqJE7i9ED/3qQl
  ..."}`
  - Requires client-side decompression (example provided below)

## PlotlyHelper

Factory for creating pre-styled Plotly charts.

### Available Chart Types
- `create_bar_chart(labels, values, title="", x_title="", y_title="")`
- `create_line_chart(x, y, title="", x_title="", y_title="")`
- `create_pie_chart(labels, values, title="")`
- `create_histogram(data, title="", x_title="", y_title="")`
- `create_scatter_plot(x, y, title="", x_title="", y_title="")`

### Example
```python
from html_renderer.plotly_helper import PlotlyHelper

# Create a bar chart
figure = PlotlyHelper.create_bar_chart(
    ["Apples", "Oranges", "Bananas"],
    [5, 3, 7],
    title="Fruit Consumption",
    x_title="Fruit",
    y_title="Quantity"
)

# Add to renderer
renderer.add_plotly_figure(figure)
```

## Output Formats

### 1. Standard HTML
```python
html = renderer.render()
```

### 2. Minified HTML (no extra whitespace)
```python
compact_html = renderer.render(compact=True)
```

### 3. JSON Output
```python
# Get HTML wrapped in JSON
json_str = renderer.render_as_json(compact=True)
# {"html": "<div class=\"content-block..."}

# Get compressed output (smaller size)
compressed = renderer.render_as_compressed_json()
# {"html_compressed": "eJx9kM1OwzAMhF9l5BQ5OYUe+gM9cYQKqVXqJE7i9ED/3qQl..."}
```

### Client-Side Decompression (JavaScript)
```javascript
function decompress(compressed) {
  const binary = atob(compressed);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  const inflate = new Zlib.Inflate(bytes);
  return new TextDecoder().decode(inflate.decompress());
}

// Usage
const data = JSON.parse(compressedJson);
const html = decompress(data.html_compressed);
document.getElementById('container').innerHTML = html;
```

## Examples

### Example 1: Simple Question with Options
```python
from html_renderer.renderer import HTMLRenderer

renderer = (
    HTMLRenderer(title="Math Quiz")
    .add_content(
        "<h2>Question 1</h2>"
        "<p>What is the capital of France?</p>",
        content_type="question"
    )
    .add_content("A. London", content_type="option")
    .add_content("B. Paris", content_type="option")
    .add_content("C. Berlin", content_type="option")
)

# Get as separate blocks for iframe embedding
blocks = renderer.render_as_blocks()
```

### Example 2: Chart with Table
```python
from html_renderer import HTMLRenderer, PlotlyHelper

# Create a sample chart
figure = PlotlyHelper.create_line_chart(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17],
    title="Sample Data",
    x_title="X Axis",
    y_title="Y Axis"
)

# Create renderer with chart and table
renderer = (
    HTMLRenderer(title="Data Analysis")
    .add_plotly_figure(figure)
    .add_table(
        data=[[1, 10], [2, 15], [3, 13], [4, 17]],
        headers=["X", "Y"]
    )
)

# Get as compressed JSON for API response
compressed_json = renderer.render_as_compressed_json()
```

## Best Practices

1. **Content Organization**
   - Use `content_type` to style questions, options, and general content differently
   - Group related blocks together using multiple `add_*` calls

2. **Performance**
   - Use `render_as_compressed_json()` for API responses to reduce bandwidth
   - Enable `compact=True` for production to minimize HTML size

3. **Frontend Integration**
   - Use iframes to isolate content and prevent CSS conflicts
   - Implement lazy loading for better performance with many blocks

4. **Caching**
   - Cache rendered HTML on the server when possible
   - Use content hashing for cache invalidation

## License
MIT
