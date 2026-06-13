from pathlib import Path
from plasTeX.PackageResource import PackageTemplateDir

PKG_DIR = Path(__file__).parent


def ProcessOptions(options, document):
    templatedir = PackageTemplateDir(
        renderers='html5',
        path=PKG_DIR / 'renderer_templates' / 'html5',
    )
    document.addPackageResource(templatedir)
