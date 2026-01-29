"""
Stylometry CLI - Quantitative author fingerprinting & stylometric analysis.

A comprehensive offline tool for extracting stylometric artifacts, computing
authorship attribution metrics, and generating interactive analysis reports.
"""

__version__ = "1.0.0"
__author__ = "SpectreDeath"

from .cli import main

__all__ = ["main", "__version__"]
