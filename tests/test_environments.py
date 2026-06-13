"""Tests that assumptions and conclusion environments parse correctly."""


def _find_node(document, nodename):
    stack = list(document.childNodes)
    while stack:
        node = stack.pop()
        if getattr(node, 'nodeName', None) == nodename:
            return node
        stack.extend(getattr(node, 'childNodes', []))
    return None


def test_assumptions_env_exists(parse):
    doc = parse(r"""\begin{assumptions}\item \ring{R}\end{assumptions}""")
    assert _find_node(doc, 'assumptions') is not None


def test_conclusion_env_exists(parse):
    doc = parse(r"""\begin{conclusion}\unit{f(r)}{S}\end{conclusion}""")
    assert _find_node(doc, 'conclusion') is not None


def test_assumptions_contains_ring(parse):
    doc = parse(r"""\begin{assumptions}\item \ring{R}\end{assumptions}""")
    asmp = _find_node(doc, 'assumptions')
    ring = _find_node(asmp, 'ring')
    assert ring is not None
    assert ring.attributes['name'].textContent.strip() == 'R'
