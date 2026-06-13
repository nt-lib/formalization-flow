"""Tests that object macros parse correctly and expose the right attributes."""


def _find_node(document, nodename):
    stack = list(document.childNodes)
    while stack:
        node = stack.pop()
        if getattr(node, 'nodeName', None) == nodename:
            return node
        stack.extend(getattr(node, 'childNodes', []))
    return None


def test_ring_parses(parse):
    doc = parse(r"\ring{R}")
    node = _find_node(doc, 'ring')
    assert node is not None
    assert node.attributes['name'].textContent.strip() == 'R'


def test_ringhom_parses(parse):
    doc = parse(r"\ringhom{f}{R}{S}")
    node = _find_node(doc, 'ringhom')
    assert node is not None
    assert node.attributes['name'].textContent.strip() == 'f'
    assert node.attributes['domain'].textContent.strip() == 'R'
    assert node.attributes['codomain'].textContent.strip() == 'S'


def test_unit_parses(parse):
    doc = parse(r"\unit{r}{R}")
    node = _find_node(doc, 'unit')
    assert node is not None
    assert node.attributes['elem'].textContent.strip() == 'r'
    assert node.attributes['ring'].textContent.strip() == 'R'


def test_ideal_parses(parse):
    doc = parse(r"\ideal{I}{R}")
    node = _find_node(doc, 'ideal')
    assert node is not None
    assert node.attributes['name'].textContent.strip() == 'I'
    assert node.attributes['ring'].textContent.strip() == 'R'


def test_module_parses(parse):
    doc = parse(r"\module{M}{R}")
    node = _find_node(doc, 'module')
    assert node is not None
    assert node.attributes['name'].textContent.strip() == 'M'
    assert node.attributes['ring'].textContent.strip() == 'R'
