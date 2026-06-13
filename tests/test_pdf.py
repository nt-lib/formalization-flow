import subprocess
import tempfile
import shutil
import os
from pathlib import Path

EXAMPLE_TEX = r"""
\documentclass{article}
\usepackage{formalizationflow}
\begin{document}

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

\end{document}
"""

STY_DIR = Path(__file__).parent.parent / "sty"


def test_pdflatex_compiles():
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "test.tex")
        with open(tex_path, "w") as f:
            f.write(EXAMPLE_TEX)
        shutil.copy(STY_DIR / "formalizationflow.sty", tmpdir)
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "test.tex"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"pdflatex failed:\n{result.stdout}"
        assert os.path.exists(os.path.join(tmpdir, "test.pdf"))
