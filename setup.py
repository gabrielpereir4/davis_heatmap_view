from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    entry_points={
        "webviz_config_plugins": [
            "Heatmap = plugins.main:Heatmap"
        ]
        
    },
)