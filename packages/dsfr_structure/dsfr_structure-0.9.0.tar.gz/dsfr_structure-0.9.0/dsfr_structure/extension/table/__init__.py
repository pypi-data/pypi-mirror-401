from xml.etree.ElementTree import Element

from markdown.extensions import Extension
from markdown.extensions.tables import TableProcessor


class DsfrTableProcessor(TableProcessor):
    def __init__(self, parser, config):
        super().__init__(parser, config)

    def run(self, parent, blocks):
        super().run(parent, blocks)

        if len(parent) > 0 and parent[-1].tag == "table":
            table = parent[-1]
            div = Element("div")
            div.set("class", "fr-table")
            div.append(table)
            parent[-1] = div

            # Add a caption following the MultiMarkdown specification
            # (https://fletcher.github.io/MultiMarkdown-5/tables.html)
            # Check caption presence : the first td of a row has the format [the caption text]
            tbody = table.find("tbody")
            if tbody is None:
                return
            for row in tbody.findall("tr"):
                first_cell = row.find("td")
                if first_cell is None:
                    continue
                caption_text = first_cell.text.strip() if first_cell.text else ""
                if caption_text.startswith("[") and caption_text.endswith("]"):
                    caption_text = caption_text[1:-1].strip()
                    caption = Element("caption")
                    caption.text = caption_text
                    table.insert(0, caption)
                    # delete the row containing the caption
                    tbody.remove(row)
                    break


class DsfrTableExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            DsfrTableProcessor(md.parser, self.getConfigs()), "table", 75
        )


def makeExtension(**kwargs):
    return DsfrTableExtension(**kwargs)
