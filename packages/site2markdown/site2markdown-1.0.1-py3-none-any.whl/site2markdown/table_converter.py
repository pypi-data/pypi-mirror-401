"""Table converter module for converting HTML tables to markdown."""

import re
import html


class TableConverter:
    """Converts HTML tables to markdown format."""
    
    MAX_WIDTH = 96

    @staticmethod
    def clean(text):
        """Clean HTML text by removing tags and decoding entities."""
        text = re.sub(r'<\/?[^>]+(>|$)', '', text)
        text = re.sub(r'(\r\n|\n|\r)', '', text)
        text = html.unescape(text)
        return text

    @staticmethod
    def ljust(text, width, fillchar=' '):
        """Left-justify text to a given width."""
        return text.ljust(width, fillchar)

    def convert(self, table_html):
        """Convert HTML table to markdown format."""
        result = "\n"

        # Extract caption if present
        caption_match = re.search(r'<caption[^>]*>((?:.|\n)*)<\/caption>', table_html, re.IGNORECASE)
        if caption_match:
            result += self.clean(caption_match.group(1)) + "\n\n"

        items = []

        # Extract table rows
        rows = re.findall(r'(<tr[^>]*>(?:.|\n)*?<\/tr>)', table_html, re.IGNORECASE)
        n_rows = len(rows) if rows else 0

        # Need at least 2 rows for a proper table
        if n_rows < 2:
            return ""

        # Extract cells from each row
        for row in rows:
            item_cols = []
            cols = re.findall(r'<t[hd][^>]*>(?:.|\n)*?<\/t[hd]>', row, re.IGNORECASE)
            for col in cols:
                item_cols.append(self.clean(col))
            items.append(item_cols)

        # Find number of columns
        n_cols = max(len(row) for row in items)

        # Normalize columns (ensure all rows have the same number of columns)
        for row in items:
            while len(row) < n_cols:
                row.append("")

        # Calculate column widths
        column_widths = [3] * n_cols
        for row in items:
            for c, cell in enumerate(row):
                if len(cell) > column_widths[c]:
                    column_widths[c] = len(cell)

        # Calculate total width
        total_width = sum(column_widths)

        if total_width < self.MAX_WIDTH:
            # Present as markdown table
            # Pad cells
            for row in items:
                for c in range(n_cols):
                    row[c] = self.ljust(row[c], column_widths[c], " ")

            if n_rows > 0 and n_cols > 0:
                # Header row
                if n_rows > 1:
                    result += "|"
                    for c in range(n_cols):
                        result += items[0][c]
                        result += "|"
                result += "\n"
                
                # Separator row
                result += "|"
                for c in range(n_cols):
                    result += "-" * column_widths[c] + "|"
                result += "\n"
                
                # Data rows
                for r in range(1, n_rows):
                    result += "|"
                    for c in range(n_cols):
                        result += items[r][c]
                        result += "|"
                    result += "\n"
        else:
            # Present as indented list
            result += "\n"
            for r in range(1, n_rows):
                if items[0][0] or items[r][0]:
                    result += "* "
                if items[0][0]:
                    result += items[0][0]
                    result += ": "
                if items[r][0]:
                    result += items[r][0]
                if items[0][0] or items[r][0]:
                    result += "\n"
                
                for c in range(1, n_cols):
                    if items[0][c] or items[r][c]:
                        result += "  * "
                    if items[0][c]:
                        result += items[0][c]
                        result += ": "
                    if items[r][c]:
                        result += items[r][c]
                    if items[0][c] or items[r][c]:
                        result += "\n"

        return result
