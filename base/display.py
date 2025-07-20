from .component import Component


class Display(Component):
    @staticmethod
    def get_component_name():
        return "display"

    def show(self, data: dict):
        raise NotImplementedError
