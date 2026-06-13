from __future__ import annotations
from pathlib import Path
import jinja2
from plasTeX.Renderers import Renderer as BaseRenderer

TEMPLATE_DIR = (
    Path(__file__).parent.parent.parent
    / 'Packages' / 'renderer_templates' / 'lean4'
)

_assumption_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR / 'assumption')),
    undefined=jinja2.Undefined,
)

_conclusion_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR / 'conclusion')),
    undefined=jinja2.Undefined,
)


def _attrs(node):
    result = {}
    for k, v in (node.attributes or {}).items():
        if hasattr(v, 'textContent'):
            result[k] = v.textContent.strip()
        else:
            result[k] = str(v).strip() if v is not None else ''
    return result


def _render_assumption(node):
    try:
        tpl = _assumption_env.get_template(node.nodeName + '.jinja2')
        return tpl.render(**_attrs(node)).strip()
    except jinja2.TemplateNotFound:
        return None


def _render_conclusion(node):
    try:
        tpl = _conclusion_env.get_template(node.nodeName + '.jinja2')
        return tpl.render(**_attrs(node)).strip()
    except jinja2.TemplateNotFound:
        return None


def _is_item_node(node):
    """Return True if node is an \\item separator."""
    return getattr(node, 'nodeName', '') == 'item'


def _has_assumption_template(node):
    """Return True if node is a known formalisation macro with an assumption template."""
    name = getattr(node, 'nodeName', '')
    return (TEMPLATE_DIR / 'assumption' / (name + '.jinja2')).exists()


def _has_conclusion_template(node):
    """Return True if node is a known macro with a conclusion template."""
    name = getattr(node, 'nodeName', '')
    return (TEMPLATE_DIR / 'conclusion' / (name + '.jinja2')).exists()


def _strip_label_prefix(label):
    """Strip LaTeX label namespace prefix (e.g. 'thm:unit_hom' -> 'unit_hom')."""
    if ':' in label:
        return label.rsplit(':', 1)[-1]
    return label


class Renderer(BaseRenderer):

    def render(self, document):
        output = self.render_to_string(document)
        jobname = document.userdata.get('jobname', 'output')
        Path(f'{jobname}.lean').write_text(output, encoding='utf-8')

    def render_to_string(self, document):
        parts = []
        self._walk(document, parts)
        return ''.join(parts)

    def _walk(self, node, parts):
        for child in getattr(node, 'childNodes', []):
            name = getattr(child, 'nodeName', '')
            if name in ('theorem', 'lemma'):
                parts.append(self._render_theorem(child))
            else:
                self._walk(child, parts)

    def _render_theorem(self, node):
        label = self._label(node)
        if not label:
            raise ValueError(
                'Theorem/lemma is missing a \\label. '
                'Every theorem and lemma must have a \\label{...}.'
            )
        params, todos = self._render_assumptions(node)
        ret = self._render_conclusion_block(node)
        prefix = '\n'.join(todos) + '\n' if todos else ''
        param_str = (' ' + ' '.join(params)) if params else ''
        return (
            f'{prefix}'
            f'theorem {label}{param_str} :\n'
            f'    {ret} := by\n'
            f'  sorry\n\n'
        )

    def _render_assumptions(self, theorem_node):
        asmp = self._find_child(theorem_node, 'assumptions')
        if asmp is None:
            return [], []
        params, todos = [], []
        # Children of assumptions are flat: item, macro/text, item, macro/text, ...
        # plasTeX renders \item as a node with nodeName == 'item'.
        children = list(getattr(asmp, 'childNodes', []))
        i = 0
        while i < len(children):
            child = children[i]
            if _is_item_node(child):
                # collect item content: nodes after this item until next item
                i += 1
                item_nodes = []
                while i < len(children) and not _is_item_node(children[i]):
                    item_nodes.append(children[i])
                    i += 1
                # Find first structured macro in item_nodes
                macro = None
                for n in item_nodes:
                    if _has_assumption_template(n):
                        macro = n
                        break
                if macro is not None:
                    rendered = _render_assumption(macro)
                    if rendered is not None:
                        params.append(rendered)
                    else:
                        todos.append(
                            f'-- TODO: no lean4 assumption template for \\{macro.nodeName}'
                        )
                else:
                    # freeform: collect text content from item nodes
                    text = ''.join(
                        getattr(n, 'textContent', '') for n in item_nodes
                    ).strip()
                    todos.append(f'-- TODO: formalise assumption: {text}')
            else:
                i += 1
        return params, todos

    def _render_conclusion_block(self, theorem_node):
        conc = self._find_child(theorem_node, 'conclusion')
        if conc is None:
            return 'True /- no conclusion -/'
        # Find first structured conclusion macro
        macro = None
        for child in getattr(conc, 'childNodes', []):
            if _has_conclusion_template(child):
                macro = child
                break
        if macro is not None:
            rendered = _render_conclusion(macro)
            if rendered is not None:
                return rendered
            return f'True /- no lean4 conclusion template for \\{macro.nodeName} -/'
        text = conc.textContent.strip()
        return f'True /- sketch: {text} -/'

    def _label(self, node):
        # \label{thm:foo} becomes a child node named 'label'
        # with attributes['label'] == 'thm:foo' (plain string)
        for child in getattr(node, 'childNodes', []):
            if getattr(child, 'nodeName', '') == 'label':
                attrs = getattr(child, 'attributes', None) or {}
                val = attrs.get('label')
                if val is not None:
                    if hasattr(val, 'textContent'):
                        val = val.textContent.strip()
                    else:
                        val = str(val).strip()
                    if val:
                        return _strip_label_prefix(val)
        # Fallbacks
        uid = getattr(node, 'id', None)
        if uid and not uid.startswith('a0000'):
            return _strip_label_prefix(uid)
        return None

    def _find_child(self, node, nodename):
        for child in getattr(node, 'childNodes', []):
            if getattr(child, 'nodeName', '') == nodename:
                return child
        return None
