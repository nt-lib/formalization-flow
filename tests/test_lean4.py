"""Tests for the Lean 4 renderer."""
import plasTeX
from plasTeX.TeX import TeX
from plasTeX.Config import defaultConfig
from formalization_flow.Renderers.lean4 import Renderer

PREAMBLE = r"""\documentclass{article}
\usepackage{formalizationflow}
\begin{document}
"""
POSTAMBLE = r"\end{document}"


def _parse_and_render(body):
    config = defaultConfig()
    config['general']['plugins'] = ['formalization_flow']
    document = plasTeX.TeXDocument(config=config)
    tex = TeX(document)
    tex.input(PREAMBLE + body + POSTAMBLE)
    tex.parse()
    return Renderer().render_to_string(document)


def test_theorem_with_label():
    output = _parse_and_render(r"""
\begin{theorem}\label{thm:unit_hom}
  \begin{assumptions}
    \item \ring{R}
    \item \ring{S}
    \item \ringhom{f}{R}{S}
    \item \unit{r}{R}
  \end{assumptions}
  \begin{conclusion}
    \unit{f(r)}{S}
  \end{conclusion}
\end{theorem}
""")
    assert 'theorem unit_hom' in output
    assert '(R : Type*) [Ring R]' in output
    assert '(S : Type*) [Ring S]' in output
    assert '(f : RingHom R S)' in output
    assert '(hr : IsUnit r)' in output
    assert 'IsUnit (f(r))' in output
    assert ':= by' in output
    assert 'sorry' in output


def test_theorem_missing_label_raises():
    import pytest
    with pytest.raises(ValueError, match=r'label'):
        _parse_and_render(r"""
\begin{theorem}
  \begin{assumptions}\item \ring{R}\end{assumptions}
  \begin{conclusion}\ring{R}\end{conclusion}
\end{theorem}
""")


def test_lemma_with_label():
    output = _parse_and_render(r"""
\begin{lemma}\label{foo}
  \begin{assumptions}\item \field{K}\end{assumptions}
  \begin{conclusion}\field{K}\end{conclusion}
\end{lemma}
""")
    assert 'theorem foo' in output
    assert '(K : Type*) [Field K]' in output


def test_freeform_assumption_becomes_comment():
    output = _parse_and_render(r"""
\begin{theorem}\label{thm:foo}
  \begin{assumptions}\item $R$ is nice\end{assumptions}
  \begin{conclusion}\ring{R}\end{conclusion}
\end{theorem}
""")
    assert '-- TODO: formalise assumption:' in output


def test_freeform_conclusion_becomes_true():
    output = _parse_and_render(r"""
\begin{theorem}\label{thm:foo}
  \begin{assumptions}\item \ring{R}\end{assumptions}
  \begin{conclusion}something hard to formalise\end{conclusion}
\end{theorem}
""")
    assert 'True' in output
    assert 'sketch' in output


def test_no_lean4_conclusion_template_falls_back():
    output = _parse_and_render(r"""
\begin{theorem}\label{thm:foo}
  \begin{assumptions}\item \ring{R}\end{assumptions}
  \begin{conclusion}\ring{R}\end{conclusion}
\end{theorem}
""")
    assert 'theorem foo' in output
    assert 'sorry' in output
