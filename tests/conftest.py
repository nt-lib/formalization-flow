import pytest
import plasTeX
from plasTeX.TeX import TeX
from plasTeX.Config import defaultConfig

PREAMBLE = r"""\documentclass{article}
\usepackage{formalizationflow}
\begin{document}
"""
POSTAMBLE = r"\end{document}"


@pytest.fixture
def parse():
    def _parse(body: str) -> plasTeX.TeXDocument:
        config = defaultConfig()
        config['general']['plugins'] = ['formalization_flow']
        document = plasTeX.TeXDocument(config=config)
        tex = TeX(document)
        tex.input(PREAMBLE + body + POSTAMBLE)
        tex.parse()
        return document
    return _parse
