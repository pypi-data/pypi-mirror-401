"""Sccde models."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from traceback import TracebackException
    from uuid import UUID


class CheckState(Enum):

    """Represent component loading check result."""

    UNCHECKED = 'UNCHECKED'
    OK = 'OK'
    ERROR = 'ERROR'


@dataclass
class ComponentInfo:

    """Component information."""

    name: str
    uuid: UUID


@dataclass
class PackageInfo:

    """Package information."""

    name: str
    uuid: UUID
    version: str
    description: str
    components: Sequence[ComponentInfo] = field(default_factory=list)


@dataclass
class ComponentValidity(ComponentInfo):

    """Component consistency information."""

    read_check: CheckState = CheckState.UNCHECKED
    read_error: None | str | TracebackException = None
    syntax_check: CheckState = CheckState.UNCHECKED
    syntax_error: None | str | TracebackException = None
    load_check: CheckState = CheckState.UNCHECKED
    load_error: None | str | TracebackException = None

    @property
    def is_valid(self) -> bool:
        """Return whether the component is valid."""
        return (self.read_check == CheckState.OK and
                self.syntax_check == CheckState.OK and
                (self.load_check in (CheckState.OK, CheckState.UNCHECKED)) )

@dataclass
class PackageValidity(PackageInfo):

    """Package consistency information."""

    components: Sequence[ComponentValidity] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Return whether the package is valid."""
        return all(compo.is_valid for compo in self.components)
