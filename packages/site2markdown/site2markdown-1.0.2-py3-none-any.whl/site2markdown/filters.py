"""Filter module for applying domain-specific filters and cleanup."""

import re
from urllib.parse import urlparse


class Filters:
    """Applies domain-specific filters and cleanup to markdown content."""

    FILTER_LIST = [
        {
            'domain': re.compile(r'.*'),  # Apply global filters to all domains
            'remove': [
                re.compile(r'\[¶\]\(#[^\s]+\s+"[^"]+"\)'),
            ],
            'replace': [
                {  # Unwanted spacing in links
                    'find': re.compile(r'\[[\n\s]*([^\]\n]*)[\n\s]*\]\(([^\)]*)\)'),
                    'replacement': r'[\1](\2)'
                },
                {  # Links stuck together
                    'find': re.compile(r'\)\['),
                    'replacement': ')\n['
                },
                {  # Missing URI scheme
                    'find': re.compile(r'\[([^\]]*)\]\(\/\/([^\)]*)\)'),
                    'replacement': r'[\1](https://\2)'
                }
            ]
        },
        {
            'domain': re.compile(r'.*\.wikipedia\.org'),
            'remove': [
                re.compile(r'\*\*\[\^\]\(#cite_ref[^\)]+\)\*\*'),
                re.compile(r'(?:\\\[)?\[edit\]\([^\s]+\s+"[^"]+"\)(?:\\\])?', re.IGNORECASE),
                re.compile(r'\^\s\[Jump up to[^\)]*\)', re.IGNORECASE),
                re.compile(r'\[[^\]]*\]\(#cite_ref[^\)]+\)'),
                re.compile(r'\[\!\[Edit this at Wikidata\].*'),
                re.compile(r'\[\!\[Listen to this article\]\([^\)]*\)\]\([^\)]*\.(mp3|ogg|oga|flac)[^\)]*\)'),
                re.compile(r'\[This audio file\]\([^\)]*\).*'),
                re.compile(r'\!\[Spoken Wikipedia icon\]\([^\)]*\)'),
                re.compile(r'\[.*\]\(.*Play audio.*\).*')
            ],
            'replace': [
                {
                    'find': re.compile(
                        r'\(https:\/\/upload.wikimedia.org\/wikipedia\/([^\/]+)\/thumb\/([^\)]+\..{3,4})\/[^\)]+\)',
                        re.IGNORECASE
                    ),
                    'replacement': r'(https://upload.wikimedia.org/wikipedia/\1/\2)'
                }
            ]
        },
        {
            'domain': re.compile(r'(?:.*\.)?medium\.com'),
            'replace': [
                {
                    'find': '(https://miro.medium.com/max/60/',
                    'replacement': '(https://miro.medium.com/max/600/'
                },
                {
                    'find': re.compile(r'\s*\[\s*!\[([^\]]+)\]\(([^\)]+)\)\s*\]\(([^\?\)]*)\?[^\)]*\)\s*'),
                    'replacement': r'\n![\1](\2)\n[\1](\3)\n\n'
                }
            ]
        },
        {
            'domain': re.compile(r'(?:.*\.)?stackoverflow\.com'),
            'remove': [
                re.compile(r'\* +Links(.|\r|\n)*Three +\|')
            ]
        }
    ]

    @staticmethod
    def strip_style_and_script_blocks(html):
        """Remove style and script blocks from HTML."""
        html = re.sub(r'<style[\s\S]*?<\/style>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<script[\s\S]*?<\/script>', '', html, flags=re.IGNORECASE)
        return html

    def filter(self, url, data, ignore_links=False):
        """
        Apply domain-specific filters to markdown data.
        
        Args:
            url: Source URL for determining domain filters
            data: Markdown content to filter
            ignore_links: Whether to remove all links
            
        Returns:
            Filtered markdown content
        """
        domain = ''
        base_address = ''
        
        if url:
            parsed_url = urlparse(url)
            if parsed_url:
                base_address = f"{parsed_url.scheme}://{parsed_url.hostname}"
                domain = parsed_url.hostname

        # Apply domain-specific filters
        for filter_item in self.FILTER_LIST:
            if filter_item['domain'].match(domain):
                # Apply remove filters
                if 'remove' in filter_item:
                    for remove_pattern in filter_item['remove']:
                        data = remove_pattern.sub('', data)
                
                # Apply replace filters
                if 'replace' in filter_item:
                    for replace_item in filter_item['replace']:
                        find_pattern = replace_item['find']
                        replacement = replace_item['replacement']
                        
                        if isinstance(find_pattern, str):
                            data = data.replace(find_pattern, replacement)
                        else:
                            data = find_pattern.sub(replacement, data)

        # Make relative URLs absolute
        data = re.sub(
            r'\[([^\]]*)\]\(\/([^\/][^\)]*)\)',
            lambda m: f"[{m.group(1)}]({base_address}/{m.group(2)})",
            data
        )

        # Remove inline links and refs if requested
        if ignore_links:
            data = re.sub(r'\[\[?([^\]]+\]?)\]\([^\)]+\)', r'\1', data)
            data = re.sub(r'[\\\[]+([0-9]+)[\\\]]+', r'[\1]', data)

        return data
