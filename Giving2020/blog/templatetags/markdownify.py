import mistune
from django import template
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


register = template.Library()


class HighlightRenderer(mistune.Renderer):
    """HighlightRenderer For Markdown."""

    def block_code(self, code, lang):
        """Block Code For HighlightRenderer."""
        if not lang:
            return f'\n<pre><code>{mistune.escape(code)}</code></pre>\n'

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()

        return highlight(code, lexer, formatter)


@register.filter
def markdown(value: str):
    md = mistune.Markdown(renderer=HighlightRenderer())
    return md(value)
