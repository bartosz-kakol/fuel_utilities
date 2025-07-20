from .component import Component


class Fuel(Component):
    @staticmethod
    def get_component_name():
        return "fuel"

    def read(self) -> dict:
        raise NotImplementedError
