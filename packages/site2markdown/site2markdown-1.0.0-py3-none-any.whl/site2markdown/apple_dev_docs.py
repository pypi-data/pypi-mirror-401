"""Apple Developer documentation parser module."""

import json
from typing import Dict, List, Any, Optional


class AppleDevDocsParser:
    """Parses Apple Developer documentation JSON format."""

    def __init__(self):
        self.dev_references = {}

    @staticmethod
    def dev_doc_url(url: str) -> str:
        """
        Convert Apple Developer page URL to JSON API URL.
        
        Args:
            url: Apple Developer documentation URL
            
        Returns:
            JSON API URL
        """
        query_parts = url.split('?')
        queryless = query_parts[0]
        
        if queryless.endswith('/'):
            queryless = queryless[:-1]
        
        parts = queryless.split("/")
        json_url = "https://developer.apple.com/tutorials/data"
        
        for i in range(3, len(parts)):
            json_url += "/" + parts[i]
        json_url += ".json"
        
        return json_url

    def parse_dev_doc_json(self, json_data: Dict[str, Any], inline_title: bool = True, 
                           ignore_links: bool = False) -> str:
        """
        Parse Apple Developer documentation JSON and convert to markdown.
        
        Args:
            json_data: Parsed JSON data
            inline_title: Whether to include title as H1
            ignore_links: Whether to remove links
            
        Returns:
            Markdown content
        """
        text = ""

        if inline_title:
            if 'metadata' in json_data:
                if 'title' in json_data['metadata']:
                    text += f"# {json_data['metadata']['title']}\n\n"

        if 'references' in json_data:
            self.dev_references = json_data['references']
        
        if 'primaryContentSections' in json_data:
            text += self.process_sections(json_data['primaryContentSections'], ignore_links)
        elif 'sections' in json_data:
            text += self.process_sections(json_data['sections'], ignore_links)
        
        return text

    def process_sections(self, sections: List[Dict[str, Any]], ignore_links: bool = False) -> str:
        """Process sections from Apple Developer documentation."""
        text = ""

        for section in sections:
            if 'kind' in section:
                if section['kind'] == 'declarations':
                    if 'declarations' in section:
                        for declaration in section['declarations']:
                            if 'tokens' in declaration:
                                token_text = ""
                                for token in declaration['tokens']:
                                    token_text += token.get('text', '')
                                text += token_text

                            if 'languages' in declaration:
                                if declaration['languages']:
                                    language_text = "\nLanguages: " + ', '.join(declaration['languages'])
                                    text += " " + language_text

                            if 'platforms' in declaration:
                                if declaration['platforms']:
                                    platform_text = "\nPlatforms: " + ', '.join(declaration['platforms'])
                                    text += " " + platform_text
                        text += "\n\n"
                
                elif section['kind'] == 'content':
                    text += self.process_content_section(section, ignore_links)

            if 'title' in section:
                if 'kind' in section and section['kind'] == 'hero':
                    text += f"# {section['title']}\n"
                else:
                    text += f"## {section['title']}"

            if 'content' in section:
                for section_content in section['content']:
                    if 'type' in section_content:
                        if section_content['type'] == 'text':
                            text += section_content['text'] + "\n"

        return text

    def process_content_section(self, section: Dict[str, Any], ignore_links: bool = False) -> str:
        """Process content section from Apple Developer documentation."""
        text = ""
        
        if 'content' not in section:
            return text

        for content in section['content']:
            if 'type' not in content:
                continue

            if content['type'] == 'paragraph':
                if 'inlineContent' in content:
                    inline_text = ""
                    for inline in content['inlineContent']:
                        if 'type' not in inline:
                            continue

                        if inline['type'] == "text":
                            inline_text += inline.get('text', '')
                        elif inline['type'] == "link":
                            if ignore_links:
                                inline_text += inline.get('title', '')
                            else:
                                title = inline.get('title', '')
                                destination = inline.get('destination', '')
                                inline_text += f"[{title}]({destination})"
                        elif inline['type'] == "reference":
                            if 'identifier' in inline:
                                identifier = inline['identifier']
                                if identifier in self.dev_references:
                                    inline_text += self.dev_references[identifier].get('title', '')
                        elif inline['type'] == 'codeVoice':
                            if 'code' in inline:
                                inline_text += f"`{inline['code']}`"
                    
                    text += inline_text + "\n\n"

            elif content['type'] == 'codeListing':
                code_text = "\n```\n"
                if 'code' in content:
                    code_text += '\n'.join(content['code'])
                code_text += "\n```\n\n"
                text += code_text

            elif content['type'] == 'unorderedList':
                if 'items' in content:
                    for list_item in content['items']:
                        text += "* " + self.process_content_section(list_item, ignore_links)

            elif content['type'] == 'orderedList':
                if 'items' in content:
                    n = 0
                    for list_item in content['items']:
                        n += 1
                        text += f"{n}. " + self.process_content_section(list_item, ignore_links)

            elif content['type'] == 'heading':
                if 'level' in content and 'text' in content:
                    text += "#" * content['level']
                    text += f" {content['text']}\n\n"

        return text
