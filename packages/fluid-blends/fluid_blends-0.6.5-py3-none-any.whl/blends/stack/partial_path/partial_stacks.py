from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from blends.stack.partial_path.bindings import _SymbolUnifyBindings
from blends.stack.partial_path.errors import (
    _raise_scope_stack_unsatisfied,
    _raise_symbol_stack_unsatisfied,
)
from blends.stack.partial_path.unification import (
    _common_prefix_len_scopes,
    _unify_scope_lhs_is_prefix_of_rhs,
    _unify_scope_rhs_is_prefix_of_lhs,
    _unify_scope_suffix_empty,
    _unify_symbol_lhs_is_prefix_of_rhs,
    _unify_symbol_rhs_is_prefix_of_lhs,
    _unify_symbol_suffix_empty,
)

if TYPE_CHECKING:
    from blends.stack.partial_path.bindings import (
        PartialScopeStackBindings,
        PartialSymbolStackBindings,
    )
    from blends.stack.partial_path.variables import (
        ScopeStackVariable,
        SymbolStackVariable,
    )


@dataclass(frozen=True, slots=True)
class PartialScopeStack:
    scopes: tuple[int, ...]
    variable: ScopeStackVariable | None

    @classmethod
    def empty(cls) -> PartialScopeStack:
        return cls(scopes=(), variable=None)

    @classmethod
    def from_variable(cls, variable: ScopeStackVariable) -> PartialScopeStack:
        return cls(scopes=(), variable=variable)

    def has_variable(self) -> bool:
        return self.variable is not None

    def can_match_empty(self) -> bool:
        return len(self.scopes) == 0

    def can_only_match_empty(self) -> bool:
        return len(self.scopes) == 0 and self.variable is None

    def contains_scopes(self) -> bool:
        return len(self.scopes) > 0

    def unify(
        self, rhs: PartialScopeStack, bindings: PartialScopeStackBindings
    ) -> PartialScopeStack:
        prefix_len = _common_prefix_len_scopes(self.scopes, rhs.scopes)
        lhs_suffix_scopes = self.scopes[prefix_len:]
        rhs_suffix_scopes = rhs.scopes[prefix_len:]

        if len(lhs_suffix_scopes) == 0 and len(rhs_suffix_scopes) == 0:
            return _unify_scope_suffix_empty(self, rhs, bindings)
        if len(rhs_suffix_scopes) == 0:
            return _unify_scope_rhs_is_prefix_of_lhs(self, rhs, lhs_suffix_scopes, bindings)
        if len(lhs_suffix_scopes) == 0:
            return _unify_scope_lhs_is_prefix_of_rhs(self, rhs, rhs_suffix_scopes, bindings)
        _raise_scope_stack_unsatisfied()
        raise AssertionError  # unreachable


@dataclass(frozen=True, slots=True)
class PartialScopedSymbol:
    symbol_id: int
    scopes: PartialScopeStack | None

    def unify(
        self, rhs: PartialScopedSymbol, bindings: PartialScopeStackBindings
    ) -> PartialScopedSymbol:
        if self.symbol_id != rhs.symbol_id:
            _raise_symbol_stack_unsatisfied()
        if (self.scopes is None) != (rhs.scopes is None):
            _raise_symbol_stack_unsatisfied()
        if self.scopes is None or rhs.scopes is None:
            return self
        unified_scopes = self.scopes.unify(rhs.scopes, bindings)
        return PartialScopedSymbol(symbol_id=self.symbol_id, scopes=unified_scopes)


@dataclass(frozen=True, slots=True)
class PartialSymbolStack:
    symbols: tuple[PartialScopedSymbol, ...]
    variable: SymbolStackVariable | None

    @classmethod
    def empty(cls) -> PartialSymbolStack:
        return cls(symbols=(), variable=None)

    @classmethod
    def from_variable(cls, variable: SymbolStackVariable) -> PartialSymbolStack:
        return cls(symbols=(), variable=variable)

    def has_variable(self) -> bool:
        return self.variable is not None

    def can_match_empty(self) -> bool:
        return len(self.symbols) == 0

    def can_only_match_empty(self) -> bool:
        return len(self.symbols) == 0 and self.variable is None

    def contains_symbols(self) -> bool:
        return len(self.symbols) > 0

    def unify(
        self,
        rhs: PartialSymbolStack,
        symbol_bindings: PartialSymbolStackBindings,
        scope_bindings: PartialScopeStackBindings,
    ) -> PartialSymbolStack:
        common_len = min(len(self.symbols), len(rhs.symbols))
        prefix = tuple(
            self.symbols[index].unify(rhs.symbols[index], scope_bindings)
            for index in range(common_len)
        )

        lhs_suffix_symbols = self.symbols[common_len:]
        rhs_suffix_symbols = rhs.symbols[common_len:]

        if len(lhs_suffix_symbols) == 0 and len(rhs_suffix_symbols) == 0:
            return _unify_symbol_suffix_empty(prefix, self, rhs, symbol_bindings, scope_bindings)
        if len(rhs_suffix_symbols) == 0:
            bindings = _SymbolUnifyBindings(
                symbol_bindings=symbol_bindings,
                scope_bindings=scope_bindings,
            )
            return _unify_symbol_rhs_is_prefix_of_lhs(
                prefix, self, rhs, lhs_suffix_symbols, bindings
            )
        if len(lhs_suffix_symbols) == 0:
            bindings = _SymbolUnifyBindings(
                symbol_bindings=symbol_bindings,
                scope_bindings=scope_bindings,
            )
            return _unify_symbol_lhs_is_prefix_of_rhs(
                prefix, self, rhs, rhs_suffix_symbols, bindings
            )
        _raise_symbol_stack_unsatisfied()
        raise AssertionError  # unreachable
