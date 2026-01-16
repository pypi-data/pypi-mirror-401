"""
site2markdown - Convert web pages to clean markdown format.

This package provides a simple interface to convert URLs and HTML content
to markdown format with support for special handling of various websites.
"""

from .urltomarkdown import UrlToMarkdown

__version__ = "1.0.1"
__all__ = ["UrlToMarkdown"]
