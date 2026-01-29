"""Data model technology interface"""

from opsorchestrator.core.decorator.class_decorators import classproperty


class Technology:
    @classproperty
    def name(self) -> str:
        """Each subclass must provide a name"""
        return self.__name__
