import os
import re
import pathlib

from setuptools import setup, find_packages

setup(
    entry_points={
        "webviz_config_plugins": [
            "Heatmap = plugins.main:Heatmap"
        ]
    },
)