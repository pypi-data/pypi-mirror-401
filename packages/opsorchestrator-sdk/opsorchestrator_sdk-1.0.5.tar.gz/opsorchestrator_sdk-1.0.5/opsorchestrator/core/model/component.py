"""Data model component"""

from opsorchestrator.core.decorator.class_decorators import classproperty


class Component:
    """Component interface to define a component within a technology"""

    @classproperty
    def name(self) -> str:
        """Each subclass must provide a name"""
        return self.__name__
