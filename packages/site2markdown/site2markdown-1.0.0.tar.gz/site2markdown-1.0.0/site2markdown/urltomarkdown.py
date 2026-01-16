"""Main UrlToMarkdown module providing the primary interface."""

from typing import Optional, Dict, Any
from .readers import ReaderFactory, HtmlReader
from .processor import Processor
from .filters import Filters


class UrlToMarkdown:
    """
    Main class for converting URLs and HTML to markdown.
    
    Example:
        >>> converter = UrlToMarkdown()
        >>> markdown = converter.convert("https://www.example.com")
        >>> print(markdown)
    """

    def __init__(self):
        """Initialize the UrlToMarkdown converter."""
        self.processor = Processor()
        self.filters = Filters()
        self.reader_factory = ReaderFactory()

    def convert(self, 
                url: str, 
                inline_title: bool = True,
                ignore_links: bool = False,
                improve_readability: bool = True,
                verify_ssl: bool = True) -> str:
        """
        Convert a URL to markdown.
        
        Args:
            url: URL to convert
            inline_title: Include page title as H1 heading (default: True)
            ignore_links: Remove all links from output (default: False)
            improve_readability: Apply readability algorithm to extract main content (default: True)
            verify_ssl: Whether to verify SSL certificates (default: True)
            
        Returns:
            Markdown content as string
            
        Raises:
            Exception: If URL cannot be fetched or converted
            
        Example:
            >>> converter = UrlToMarkdown()
            >>> markdown = converter.convert(
            ...     "https://www.example.com",
            ...     inline_title=True,
            ...     ignore_links=False
            ... )
        """
        options = {
            'inline_title': inline_title,
            'ignore_links': ignore_links,
            'improve_readability': improve_readability
        }
        
        reader = self.reader_factory.reader_for_url(url)
        return reader.read_url(url, options, verify_ssl=verify_ssl)

    def convert_html(self,
                     html: str,
                     url: Optional[str] = None,
                     inline_title: bool = True,
                     ignore_links: bool = False,
                     improve_readability: bool = True) -> str:
        """
        Convert HTML content to markdown.
        
        Args:
            html: HTML content to convert
            url: Base URL for resolving relative links (optional)
            inline_title: Include page title as H1 heading (default: True)
            ignore_links: Remove all links from output (default: False)
            improve_readability: Apply readability algorithm to extract main content (default: True)
            
        Returns:
            Markdown content as string
            
        Example:
            >>> converter = UrlToMarkdown()
            >>> html = "<html><body><h1>Title</h1><p>Content</p></body></html>"
            >>> markdown = converter.convert_html(
            ...     html,
            ...     url="https://www.example.com"
            ... )
        """
        options = {
            'inline_title': inline_title,
            'ignore_links': ignore_links,
            'improve_readability': improve_readability
        }
        
        # Strip style and script blocks
        html = self.filters.strip_style_and_script_blocks(html)
        
        # Process HTML
        markdown, _ = self.processor.process_dom(url, html, "", options)
        
        return markdown
