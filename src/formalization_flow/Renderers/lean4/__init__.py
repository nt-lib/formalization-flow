from plasTeX.Renderers import Renderer as BaseRenderer


class Renderer(BaseRenderer):
    def render(self, document):
        raise NotImplementedError
