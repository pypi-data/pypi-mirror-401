# site2markdown

A robust Python utility to convert web pages into clean, structured Markdown. Optimized for generating high-quality context for Large Language Models (LLMs).

## Installation

```bash
pip install site2markdown
```

## Usage

![site2markdown usage example](doc-site2md.png)

### Quick Start
```python
from site2markdown import UrlToMarkdown

converter = UrlToMarkdown()

# Convert URL to Markdown
markdown = converter.convert(
    url="https://www.example.com",
    inline_title=True,        # Include the page title as an H1
    ignore_links=False,       # Preserve hyper-links
    improve_readability=True  # Use readability algorithm to filter boilerplate
)

print(markdown)
```

### Converting HTML Content
```python
from site2markdown import UrlToMarkdown

converter = UrlToMarkdown()
html_content = "<html><body><h1>Example</h1><p>Text content.</p></body></html>"

markdown = converter.convert_html(
    html=html_content,
    url="https://www.example.com",  # Optional: base URL for resolving relative paths
    inline_title=True,
    improve_readability=True
)

print(markdown)
```

## Core Features

- **LLM Optimized**: Produces clean text with minimal noise, ideal for RAG and LLM context.
- **Smart Filtering**: Automatic removal of scripts, styles, and non-content elements.
- **Specialized Handling**: Custom parsing logic for sites like Stack Overflow, Wikipedia, and Medium.
- **Readability Engine**: Integration with Mozilla's Readability algorithm to extract the main article body and skip navigation/sidebars.
- **Structure Preservation**: Reliable conversion of code blocks, tables, and nested lists.
- **URL Resolution**: Automatically converts relative links and image paths to absolute URLs.

## Configuration Options

| Option | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| `inline_title` | `bool` | Includes the page title as an H1 heading at the top. | `True` |
| `ignore_links` | `bool` | Removes all hyperlinks from the output. | `False` |
| `improve_readability` | `bool` | Processes the page through a readability filter before conversion. | `True` |

## License

This project is licensed under the MIT License.

