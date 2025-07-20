from typing import Any, Type
import importlib
import logging

from base import Component


ComponentType = Type[Component] | str


def component_type_to_str(component: ComponentType) -> str:
    if isinstance(component, str):
        return component

    return component.get_component_name()


class ImplementationManager:
    _implementation_modules: dict[str, Any]
    _implementation_instances: dict[str, Any]

    def __init__(self):
        self._implementation_modules = {}
        self._implementation_instances = {}

    def _import_implementation(self, component: ComponentType, name: str, overwrite: bool = False):
        component_name = component_type_to_str(component)

        if component_name in self._implementation_modules and not overwrite:
            logging.debug(f"`overwrite` set to False - reusing \"{component_name}\" implementation named \"{name}\".")
            return

        module = importlib.import_module(f"impl.{component_name}.{name}")

        if "export" not in dir(module):
            raise ImportError(
                f"The target \"{component_name}\" implementation named \"{name}\" does not define its class as 'export'."
                f"Make sure to define 'export' in the module with the implementation class as the value!"
            )

        self._implementation_modules[component_name] = module

    def _create_implementation_instance(self, component: ComponentType, kwargs: dict[str, Any], overwrite: bool = False):
        component_name = component_type_to_str(component)

        if component_name in self._implementation_instances and not overwrite:
            logging.debug(f"`overwrite` set to False - reusing \"{component_name}\" implementation instance.")
            return

        if component_name not in self._implementation_modules:
            raise ValueError(f"The target \"{component_name}\" implementation has not been imported yet!")

        module = self._implementation_modules[component_name]
        implementation_class = getattr(module, "export")

        self._implementation_instances[component_name] = implementation_class(**kwargs)

    def use_implementation(self, component: ComponentType, name: str, kwargs: dict[str, Any], overwrite: bool = False):
        logging.info(f"Using \"{name}\" implementation for \"{component_type_to_str(component)}\".")

        self._import_implementation(component, name, overwrite)
        self._create_implementation_instance(component, kwargs, overwrite)

    def get_component[T: Component](self, component: Type[T]) -> T:
        component_name = component_type_to_str(component)

        if component_name not in self._implementation_instances:
            raise ValueError(f"The target \"{component_name}\" implementation has not been specified yet!")

        return self._implementation_instances[component_name]
