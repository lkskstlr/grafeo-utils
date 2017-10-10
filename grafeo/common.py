from typing import NamedTuple


"""Separators used for serialization

Separator.field between high level fields
Separator.list within a list
"""
Separators = NamedTuple('Separators', [('field', str), ('list', str)])
separators = Separators(';;', ',,')


"""The current version"""
current_version_major = 0
current_version_minor = 0
current_version_patch = 0
