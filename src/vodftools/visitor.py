#!/usr/bin/env python3
"""Defines Visitor design pattern."""


def get_class_hierarchy(cls: type):
    """Return a list of parent classes in parent to child order."""
    for base in cls.__bases__:
        yield from get_class_hierarchy(base)
        if cls is not object:
            yield cls


class Visitor:
    """Simple visitor wrapper for separating data structure from output."""

    def __init__(self, f):
        self.f = f
        self.generators = {}

    def generator(self, cls: type):
        """Define the generator."""

        def call(fun):
            self.generators[cls] = fun

        return call

    def __call__(self, obj):
        """Visit the thing."""
        classes = list(get_class_hierarchy(type(obj)))
        if len(classes) == 0:
            raise NotImplementedError(
                f"No implementation was found to convert object of type '{type(obj)}'"
            )
        for cls in classes:
            if cls in self.generators:
                yield from self.generators[cls](obj)
