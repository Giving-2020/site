from django import template
import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


register = template.Library()


class HighlightRenderer(mistune.Renderer):

    def block_code(self, code, lang):
        if not lang:
            return f'\n<pre><code>{mistune.escape(code)}</code></pre>\n'

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()

        return highlight(code, lexer, formatter)


@register.filter
def markdown(value):
    md = mistune.Markdown(renderer=HighlightRenderer())
    return md(value)
