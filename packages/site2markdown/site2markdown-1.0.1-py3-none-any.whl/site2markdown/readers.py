"""Reader module for fetching and processing URLs."""

import requests
import json
from typing import Optional, Dict, Any
from .processor import Processor
from .filters import Filters


class BaseReader:
    """Base class for URL readers."""
    
    TIMEOUT = 15
    USER_AGENT = "Urltomarkdown/1.0"

    def __init__(self):
        self.processor = Processor()
        self.filters = Filters()

    def fetch_url(self, url: str, verify_ssl: bool = True) -> str:
        """
        Fetch content from URL.
        
        Args:
            url: URL to fetch
            verify_ssl: Whether to verify SSL certificates (default: True)
            
        Returns:
            Response content as string
            
        Raises:
            requests.RequestException: If request fails
        """
        headers = {'User-Agent': self.USER_AGENT}
        response = requests.get(url, headers=headers, timeout=self.TIMEOUT, verify=verify_ssl)
        response.raise_for_status()
        return response.text

    def read_url(self, url: str, options: Optional[Dict[str, Any]] = None, verify_ssl: bool = True) -> str:
        """
        Read URL and convert to markdown.
        
        Args:
            url: URL to convert
            options: Conversion options
            verify_ssl: Whether to verify SSL certificates
            
        Returns:
            Markdown content
        """
        raise NotImplementedError("Subclasses must implement read_url")


class HtmlReader(BaseReader):
    """Reader for generic HTML pages."""

    def read_url(self, url: str, options: Optional[Dict[str, Any]] = None, verify_ssl: bool = True) -> str:
        """
        Read HTML page and convert to markdown.
        
        Args:
            url: URL to convert
            options: Conversion options
            verify_ssl: Whether to verify SSL certificates
            
        Returns:
            Markdown content
        """
        if options is None:
            options = {}

        try:
            html = self.fetch_url(url, verify_ssl=verify_ssl)
            html = self.filters.strip_style_and_script_blocks(html)
            markdown, _ = self.processor.process_dom(url, html, "", options)
            return markdown
        except Exception as e:
            raise Exception(f"Failed to fetch and convert URL: {str(e)}")


class StackReader(BaseReader):
    """Reader for Stack Overflow questions."""

    def read_url(self, url: str, options: Optional[Dict[str, Any]] = None, verify_ssl: bool = True) -> str:
        """
        Read Stack Overflow question and convert to markdown.
        
        Args:
            url: Stack Overflow question URL
            options: Conversion options
            verify_ssl: Whether to verify SSL certificates
            
        Returns:
            Markdown content including question and answer
        """
        if options is None:
            options = {}

        try:
            html = self.fetch_url(url, verify_ssl=verify_ssl)
            html = self.filters.strip_style_and_script_blocks(html)
            
            # Get question
            markdown_q, _ = self.processor.process_dom(url, html, 'question', options)
            
            # Get answer
            answer_options = options.copy()
            answer_options['inline_title'] = False
            markdown_a, _ = self.processor.process_dom(url, html, 'answers', answer_options)
            
            if markdown_a.startswith('Your Answer'):
                return markdown_q
            else:
                return markdown_q + "\n\n## Answer\n" + markdown_a
        except Exception as e:
            raise Exception(f"Failed to fetch and convert Stack Overflow page: {str(e)}")


class ReaderFactory:
    """Factory for creating appropriate reader based on URL."""
    
    STACKOVERFLOW_PREFIX = "https://stackoverflow.com/questions"

    @staticmethod
    def reader_for_url(url: str) -> BaseReader:
        """
        Get appropriate reader for URL.
        
        Args:
            url: URL to determine reader for
            
        Returns:
            Appropriate reader instance
        """
        if url.startswith(ReaderFactory.STACKOVERFLOW_PREFIX):
            return StackReader()
        else:
            return HtmlReader()

    @staticmethod
    def ignore_post(url: Optional[str]) -> bool:
        """
        Check if URL should ignore POST data and fetch directly.
        
        Args:
            url: URL to check
            
        Returns:
            True if URL should be fetched directly
        """
        if url:
            return url.startswith(ReaderFactory.STACKOVERFLOW_PREFIX)
        return False
