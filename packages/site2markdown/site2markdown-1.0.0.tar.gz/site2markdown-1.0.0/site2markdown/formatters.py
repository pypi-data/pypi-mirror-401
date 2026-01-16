"""Formatter module for handling HTML tables and code blocks."""

import re
import html as html_lib
from .table_converter import TableConverter


class Formatters:
    """Handles formatting of tables and code blocks before markdown conversion."""

    def __init__(self):
        self.table_converter = TableConverter()

    def format_tables(self, html, replacements):
        """
        Extract tables from HTML and replace with placeholders.
        
        Args:
            html: HTML string
            replacements: List to store replacement mappings
            
        Returns:
            HTML with tables replaced by placeholders
        """
        start = len(replacements)
        tables = re.findall(r'(<table[^>]*>(?:.|\n)*?<\/table>)', html, re.IGNORECASE)
        
        if tables:
            for t, table in enumerate(tables):
                markdown = self.table_converter.convert(table)
                placeholder = f"urltomarkdowntableplaceholder{t}{id(table)}"
                replacements.append({
                    'placeholder': placeholder,
                    'replacement': markdown
                })
                html = html.replace(table, f"<p>{placeholder}</p>", 1)
        
        return html

    def format_codeblocks(self, html, replacements):
        """
        Extract code blocks from HTML and replace with placeholders.
        
        Args:
            html: HTML string
            replacements: List to store replacement mappings
            
        Returns:
            HTML with code blocks replaced by placeholders
        """
        start = len(replacements)
        codeblocks = re.findall(r'(<pre[^>]*>(?:.|\n)*?<\/pre>)', html, re.IGNORECASE)
        
        if codeblocks:
            for c, codeblock in enumerate(codeblocks):
                filtered = codeblock
                filtered = re.sub(r'<br[^>]*>', '\n', filtered)
                filtered = re.sub(r'<p>', '\n', filtered)
                filtered = re.sub(r'<\/?[^>]+(>|$)', '', filtered)
                filtered = html_lib.unescape(filtered)
                
                markdown = f"```\n{filtered}\n```\n"
                placeholder = f"urltomarkdowncodeblockplaceholder{c}{id(codeblock)}"
                replacements.append({
                    'placeholder': placeholder,
                    'replacement': markdown
                })
                html = html.replace(codeblock, f"<p>{placeholder}</p>", 1)
        
        return html
