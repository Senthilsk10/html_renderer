from html_renderer.renderer import HTMLRenderer
from html_renderer.plotly_helper import PlotlyHelper

# Example usage functions
def create_math_question_example():
    """Example of a math question with LaTeX and a plot."""
    # Question with LaTeX
    question_content = r"""
    <h3>Function Analysis</h3>
    <p>Consider the quadratic function: $$f(x) = ax^2 + bx + c$$</p>
    <p>Where $a = 1$, $b = -4$, and $c = 3$</p>
    """
    
    # Create a plot of the quadratic function
    import numpy as np
    x = np.linspace(-1, 5, 100)
    y = x**2 - 4*x + 3
    
    fig = PlotlyHelper.create_line_chart(
        x_data=x.tolist(),
        y_data=y.tolist(),
        title="f(x) = x² - 4x + 3",
        x_label="x",
        y_label="f(x)",
        color="#2e86c1"
    )
    
    # Add horizontal line at y=0
    fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.7)
    
    renderer = HTMLRenderer(title="Math Question")
    renderer.add_content(question_content, content_type="question") \
            .add_plotly_figure(fig) \
            .add_content("Based on the graph above, what are the x-intercepts of this function?") \
            

    # Options
    options = [
        r"$x = 1$ and $x = 3$",
        r"$x = 2$ and $x = 4$",
        r"$x = 0$ and $x = 2$",
        r"$x = -1$ and $x = 5$"
    ]

    for option in options:
        renderer.add_content(option, content_type="option")
    
    return renderer.render()

def create_data_analysis_example():
    """Example of a data analysis question with charts."""
    question_content = """
    <h3>Sales Data Analysis</h3>
    <p>The chart below shows the monthly sales data for a company over 6 months.</p>
    <p>Which month showed the highest percentage increase compared to the previous month?</p>
    """
    
    # Create sales data chart
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    sales = [12000, 15000, 14000, 18000, 22000, 25000]
    
    fig = PlotlyHelper.create_bar_chart(
        x_data=months,
        y_data=sales,
        title="Monthly Sales Data",
        x_label="Month",
        y_label="Sales ($)",
        color="#27ae60"
    )
    
    renderer = HTMLRenderer(title="Data Analysis Question")
    renderer.add_content(question_content, content_type="question") \
            .add_plotly_figure(fig)
    
    # Options with individual charts showing percentage changes
    option_texts = ["February (+25%)", "March (-6.7%)", "April (+28.6%)", "May (+22.2%)"]
    
    for text in option_texts:
        renderer.add_content(f"<p><strong>{text}</strong></p>", content_type="option")
    
    return renderer.render()

def create_statistics_example():
    """Example combining statistics with visualization."""
    question_content = r"""
    <h3>Statistical Distribution</h3>
    <p>The histogram below shows the distribution of test scores for a class of students.</p>
    <p>Based on a normal distribution: $$\mu = \frac{1}{n}\sum_{i=1}^{n} x_i$$</p>
    """
    
    # Create histogram of test scores
    import numpy as np
    np.random.seed(42)
    scores = np.random.normal(78, 12, 100)  # Mean=78, std=12
    
    fig = PlotlyHelper.create_histogram(
        data=scores.tolist(),
        title="Test Score Distribution",
        x_label="Score",
        bins=15
    )
    
    renderer = HTMLRenderer(title="Statistics Question")
    renderer.add_content(question_content, content_type="question") \
            .add_plotly_figure(fig)
    
    options = [
        "Approximately 65",
        "Approximately 78",
        "Approximately 85",
        "Approximately 92"
    ]

    for option in options:
        renderer.add_content(option, content_type="option")
    
    return renderer.render()

def create_pie_chart_example():
    """Example of a question with a pie chart."""
    question_content = """
    <h3>Market Share Analysis</h3>
    <p>The pie chart below shows the market share of different smartphone brands.</p>
    <p>Which brand has the second-largest market share?</p>
    """
    
    labels = ['Brand A', 'Brand B', 'Brand C', 'Brand D', 'Others']
    values = [35, 28, 18, 12, 7]
    
    fig = PlotlyHelper.create_pie_chart(
        labels=labels,
        values=values,
        title="Smartphone Market Share"
    )
    
    renderer = HTMLRenderer(title="Pie Chart Question")
    renderer.add_content(question_content, content_type="question") \
            .add_plotly_figure(fig)
    
    options = [
        "Brand A",
        "Brand B",
        "Brand C",
        "Brand D"
    ]

    for option in options:
        renderer.add_content(option, content_type="option")

    return renderer.render()

def create_table_example():
    """Example of a document with a table."""
    renderer = HTMLRenderer(title="Table Example")
    renderer.add_content("<h3>Here is a table of student data:</h3>") \
            .add_table(
                headers=["ID", "Name", "Grade"],
                data=[
                    [1, "Alice", 85],
                    [2, "Bob", 92],
                    [3, "Charlie", 78]
                ]
            )
    return renderer.render()

def create_combined_example():
    """Example combining multiple plots and a table."""
    renderer = HTMLRenderer(title="Combined Report")
    renderer.add_content("<h2>Combined Report</h2>") \
            .add_content("<p>This report contains a bar chart, a pie chart, and a data table.</p>") \
            .add_plotly_figure(PlotlyHelper.create_bar_chart(
                x_data=["A", "B", "C","D","E","F"],
                y_data=[10, 12, 15,25,20,22],
                title="Bar Chart"
            )) \
            .add_plotly_figure(PlotlyHelper.create_pie_chart(
                labels=["X", "Y", "Z"],
                values=[40, 30, 30],
                title="Pie Chart"
            )) \
            .add_table(
                headers=["Product", "Price", "In Stock"],
                data=[
                    ["Apple", 1.50, True],
                    ["Banana", 4.75, True],
                    ["Orange", 1.25, False],
                    ["Mango", 1.75, False]
                ]
            )
    return renderer.render()


if __name__ == "__main__":
    print(create_math_question_example())