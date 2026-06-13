from pathlib import Path
from plasTeX import Command, Environment
from plasTeX.PackageResource import PackageTemplateDir

PKG_DIR = Path(__file__).parent


class ring(Command):
    args = 'name'


class commring(Command):
    args = 'name'


class field(Command):
    args = 'name'


class ringhom(Command):
    args = 'name domain codomain'


class unit(Command):
    args = 'elem ring'


class ideal(Command):
    args = 'name ring'


class module(Command):
    args = 'name ring'


class theorem(Environment):
    pass


class lemma(Environment):
    pass


class assumptions(Environment):
    pass


class conclusion(Environment):
    pass


def ProcessOptions(options, document):
    templatedir = PackageTemplateDir(
        renderers='html5',
        path=PKG_DIR / 'renderer_templates' / 'html5',
    )
    document.addPackageResource(templatedir)
