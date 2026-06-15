# formalization-flow

A plasTeX plugin and LaTeX style that lets a mathematician write one `.tex` file and build it
three ways:

- `pdflatex main.tex` -- PDF
- `plastex main.tex` -- HTML
- `plastex --renderer lean4 main.tex` -- sorry-filled Lean 4 skeleton

**Status:** Alpha -- breaking changes expected until stabilisation.

## Requirements

- Python >= 3.9
- plasTeX >= 3.1
- Jinja2 >= 3.1.0
- pdflatex (for PDF output)
- pytest (for tests; included in the `dev` extra)


## Installation

```bash
make venv          # creates .venv and pip install -e ".[dev]"
```

Or manually:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Running the example

```bash
make example
```

This runs three builds of `examples/unit_hom.tex`:

1. `pdflatex` -- produces `examples/unit_hom.pdf`
2. `plastex` -- produces `examples/unit_hom/index.html`
3. `plastex --renderer lean4` -- produces a `.lean` file

## Running tests

```bash
make test
```

## Macro vocabulary

Each macro declares one mathematical object. In PDF/HTML it renders as a "Let ... be ..." sentence;
in Lean 4 it maps to a parameter declaration or typeclass constraint.

| Macro | PDF/HTML | Lean 4 (assumption) |
|-------|----------|---------------------|
| `\ring{R}` | Let *R* be a ring. | `(R : Type*) [Ring R]` |
| `\commring{R}` | Let *R* be a commutative ring. | `(R : Type*) [CommRing R]` |
| `\field{K}` | Let *K* be a field. | `(K : Type*) [Field K]` |
| `\ringhom{f}{R}{S}` | Let *f* : *R* -> *S* be a ring homomorphism. | `(f : R ->+* S)` |
| `\unit{r}{R}` | Let *r* in *R*^x be a unit. | `(hr : IsUnit r)` |
| `\ideal{I}{R}` | Let *I* be an ideal of *R*. | `(I : Ideal R)` |
| `\module{M}{R}` | Let *M* be an *R*-module. | `(M : Type*) [Module R M]` |

## Environments

`assumptions` -- an itemised list of hypotheses (structured macros or free-form text):

```latex
\begin{assumptions}
  \item \ring{R}
  \item \ringhom{f}{R}{S}
\end{assumptions}
```

`conclusion` -- the theorem's return type:

```latex
\begin{conclusion}
  \unit{f(r)}{S}
\end{conclusion}
```

Free-form `\item` text (not a structured macro) renders as-is in PDF/HTML and becomes
`-- TODO: formalise assumption: <text>` in Lean 4. A free-form conclusion becomes
`True /- sketch: <text> -/`.

## Lean 4 output format

For each `theorem`/`lemma` environment the renderer emits:

```lean
theorem <label> <assumptions> :
    <conclusion> := by
  sorry
```

`\label` is required on every theorem and lemma; the renderer raises an error if it is missing.

Example -- given `examples/unit_hom.tex`:

```latex
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
```

Lean 4 output:

```lean
theorem unit_hom (R : Type*) [Ring R] (S : Type*) [Ring S] (f : R ->+* S) (hr : IsUnit r) :
    IsUnit (f(r)) := by
  sorry
```

## Architecture

Command classes in `formalizationflow.py` are thin shells that only declare argument structure
(`args`). No rendering logic lives in Python -- it all lives in Jinja2 template files. Adding a
new mathematical object means adding template files only; no Python changes are required.

To add `\group{G}` mapping to `(G : Type*) [Group G]`:

1. Add `\newcommand{\group}[1]{Let $#1$ be a group.}` to `sty/formalizationflow.sty`.
2. Add `src/formalization_flow/Packages/renderer_templates/html5/group.jinja2`.
3. Add `src/formalization_flow/Packages/renderer_templates/lean4/assumption/group.jinja2`.
4. Add a `group` Command class to `formalizationflow.py` with `args = 'name'`.

## Known limitations (alpha)

- HTML Jinja2 templates use `self.attributes.name`; this may need adjustment depending on the
  installed plasTeX version.
- The nodeName for `\item` inside `assumptions` may differ across plasTeX versions (`@item`).
- `\label` extraction may need adjustment; check `thm.attributes` and `thm.userdata` if labels
  are not found.
- Lean 4 output file path is controlled by plasTeX's output config; use `plastex.cfg` to
  override.

## Related projects

- [Lean Blueprint](https://github.com/PatrickMassot/leanblueprint) -- tracks formalization
  progress; intended to be combinable.
- [plasTeX](https://github.com/plastex/plastex/) -- the Python LaTeX parser this builds on.

## Project layout

| Path | Contents |
|------|----------|
| `src/formalization_flow/Packages/` | plasTeX macro and environment definitions (`formalizationflow.py`) |
| `src/formalization_flow/Packages/renderer_templates/html5/` | Jinja2 templates for HTML rendering |
| `src/formalization_flow/Packages/renderer_templates/lean4/` | Jinja2 templates for Lean 4 rendering (`assumption/` and `conclusion/`) |
| `src/formalization_flow/Renderers/lean4/` | Lean 4 renderer (walks parse tree, emits `.lean`) |
| `sty/` | `formalizationflow.sty` -- LaTeX style for PDF via pdflatex |
| `examples/` | `unit_hom.tex` motivating example + `plastex.cfg` |
| `tests/` | pytest suite (macros, environments, Lean 4 renderer, PDF smoke test) |
| `docs/` | Design spec and MVP implementation plan |
