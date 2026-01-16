from __future__ import annotations

from enum import Enum
from typing import NoReturn


class PartialPathResolutionErrorCode(str, Enum):
    SCOPE_STACK_UNSATISFIED = "ScopeStackUnsatisfied"
    SYMBOL_STACK_UNSATISFIED = "SymbolStackUnsatisfied"


class PartialPathResolutionError(Exception):
    @property
    def code(self) -> PartialPathResolutionErrorCode:
        first_arg = (
            self.args[0] if self.args else PartialPathResolutionErrorCode.SYMBOL_STACK_UNSATISFIED
        )
        return (
            first_arg
            if isinstance(first_arg, PartialPathResolutionErrorCode)
            else PartialPathResolutionErrorCode.SYMBOL_STACK_UNSATISFIED
        )


def _raise_scope_stack_unsatisfied() -> NoReturn:
    raise PartialPathResolutionError(PartialPathResolutionErrorCode.SCOPE_STACK_UNSATISFIED)


def _raise_symbol_stack_unsatisfied() -> NoReturn:
    raise PartialPathResolutionError(PartialPathResolutionErrorCode.SYMBOL_STACK_UNSATISFIED)
