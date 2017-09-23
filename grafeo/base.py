from typing import NamedTuple


"""Separators used for serialization

Separator.field between high level fields
Separator.list within a list
"""
Separators = NamedTuple('Separators', [('field', str), ('list', str)])
separators = Separators(';;', ',,')

"""Version"""
Version = NamedTuple('Version', [('major', int), ('minor', int), ('patch', int)])


def version_to_str(version: Version) -> str:
    return separators.list.join([
        str(version.major),
        str(version.minor),
        str(version.patch)
    ])

"""The current version"""
current_version = Version(major=0, minor=0, patch=0)
