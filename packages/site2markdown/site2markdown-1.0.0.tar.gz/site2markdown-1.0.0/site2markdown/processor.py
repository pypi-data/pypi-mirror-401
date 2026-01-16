"""Processor module for converting HTML DOM to markdown."""

import html2text
from bs4 import BeautifulSoup
from readability import Document
from urllib.parse import quote
from .formatters import Formatters
from .filters import Filters


class Processor:
    """Processes HTML DOM and converts to markdown."""

    def __init__(self):
        self.formatters = Formatters()
        self.filters = Filters()
        self.html2text_converter = html2text.HTML2Text()
        self.html2text_converter.body_width = 0  # Don't wrap text
        self.html2text_converter.ignore_images = False
        self.html2text_converter.ignore_links = False

    def process_dom(self, url, html_content, element_id="", options=None):
        """
        Process HTML content and convert to markdown.
        
        Args:
            url: Source URL
            html_content: HTML content as string
            element_id: Optional element ID to extract (e.g., for Stack Overflow)
            options: Dictionary with conversion options
            
        Returns:
            Tuple of (markdown_content, title)
        """
        if options is None:
            options = {}

        inline_title = options.get('inline_title', True)
        ignore_links = options.get('ignore_links', False)
        improve_readability = options.get('improve_readability', True)

        # Parse HTML
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Extract title
        title_element = soup.find('title')
        title = title_element.get_text() if title_element else ""

        # Extract specific element if ID is provided
        if element_id:
            element = soup.find(id=element_id)
            if element:
                html_content = str(element)
                soup = BeautifulSoup(html_content, 'lxml')

        # Apply readability if requested
        readable = None
        if improve_readability:
            try:
                doc = Document(html_content)
                readable = doc.summary()
            except Exception:
                readable = None

        if not readable:
            readable = str(soup)

        # Format code blocks and tables
        replacements = []
        readable = self.formatters.format_codeblocks(readable, replacements)
        readable = self.formatters.format_tables(readable, replacements)

        # Convert to markdown
        markdown = self.html2text_converter.handle(readable)

        # Restore formatted code blocks and tables
        for replacement in replacements:
            markdown = markdown.replace(replacement['placeholder'], replacement['replacement'])

        # Apply filters
        result = self.filters.filter(url, markdown, ignore_links) if url else markdown

        # Add title if requested
        if inline_title and title:
            result = f"# {title}\n{result}"

        return result, title
