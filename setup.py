from setuptools import setup, find_packages

setup(
    name="html_renderer",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'plotly',
        'jinja2',
    ],
)
