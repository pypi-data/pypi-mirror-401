from __future__ import annotations

from typing import TYPE_CHECKING

from blends.stack.partial_path.errors import (
    _raise_scope_stack_unsatisfied,
    _raise_symbol_stack_unsatisfied,
)
from blends.stack.partial_path.partial_stacks import (
    PartialScopedSymbol,
    PartialScopeStack,
    PartialSymbolStack,
)

if TYPE_CHECKING:
    from blends.stack.partial_path.bindings import (
        PartialScopeStackBindings,
        PartialSymbolStackBindings,
        _SymbolUnifyBindings,
    )


def _common_prefix_len_scopes(lhs: tuple[int, ...], rhs: tuple[int, ...]) -> int:
    prefix_len = 0
    for lhs_scope, rhs_scope in zip(lhs, rhs, strict=False):
        if lhs_scope != rhs_scope:
            _raise_scope_stack_unsatisfied()
        prefix_len += 1
    return prefix_len


def _unify_scope_suffix_empty(
    lhs: PartialScopeStack, rhs: PartialScopeStack, bindings: PartialScopeStackBindings
) -> PartialScopeStack:
    lhs_var = lhs.variable
    rhs_var = rhs.variable
    if lhs_var is None and rhs_var is None:
        return lhs
    if lhs_var is None and rhs_var is not None:
        bindings.add(rhs_var, PartialScopeStack.empty())
        return rhs
    if lhs_var is not None and rhs_var is None:
        bindings.add(lhs_var, PartialScopeStack.empty())
        return lhs
    if lhs_var is None or rhs_var is None:
        _raise_scope_stack_unsatisfied()
    bindings.add(rhs_var, PartialScopeStack.from_variable(lhs_var))
    return lhs


def _unify_scope_rhs_is_prefix_of_lhs(
    lhs: PartialScopeStack,
    rhs: PartialScopeStack,
    lhs_suffix_scopes: tuple[int, ...],
    bindings: PartialScopeStackBindings,
) -> PartialScopeStack:
    rhs_var = rhs.variable
    if rhs_var is None:
        _raise_scope_stack_unsatisfied()
    if lhs.variable is not None and lhs.variable == rhs_var:
        _raise_scope_stack_unsatisfied()
    bindings.add(rhs_var, PartialScopeStack(scopes=lhs_suffix_scopes, variable=lhs.variable))
    return lhs


def _unify_scope_lhs_is_prefix_of_rhs(
    lhs: PartialScopeStack,
    rhs: PartialScopeStack,
    rhs_suffix_scopes: tuple[int, ...],
    bindings: PartialScopeStackBindings,
) -> PartialScopeStack:
    lhs_var = lhs.variable
    if lhs_var is None:
        _raise_scope_stack_unsatisfied()
    if rhs.variable is not None and rhs.variable == lhs_var:
        _raise_scope_stack_unsatisfied()
    bindings.add(lhs_var, PartialScopeStack(scopes=rhs_suffix_scopes, variable=rhs.variable))
    return rhs


def _unify_symbol_suffix_empty(
    prefix: tuple[PartialScopedSymbol, ...],
    lhs: PartialSymbolStack,
    rhs: PartialSymbolStack,
    symbol_bindings: PartialSymbolStackBindings,
    scope_bindings: PartialScopeStackBindings,
) -> PartialSymbolStack:
    lhs_var = lhs.variable
    rhs_var = rhs.variable
    if lhs_var is None and rhs_var is None:
        return PartialSymbolStack(symbols=prefix, variable=None)
    if lhs_var is None and rhs_var is not None:
        symbol_bindings.add(rhs_var, PartialSymbolStack.empty(), scope_bindings)
        return PartialSymbolStack(symbols=prefix, variable=rhs_var)
    if lhs_var is not None and rhs_var is None:
        symbol_bindings.add(lhs_var, PartialSymbolStack.empty(), scope_bindings)
        return PartialSymbolStack(symbols=prefix, variable=lhs_var)
    if lhs_var is None or rhs_var is None:
        _raise_symbol_stack_unsatisfied()
    symbol_bindings.add(rhs_var, PartialSymbolStack.from_variable(lhs_var), scope_bindings)
    return PartialSymbolStack(symbols=prefix, variable=lhs_var)


def _unify_symbol_rhs_is_prefix_of_lhs(
    prefix: tuple[PartialScopedSymbol, ...],
    lhs: PartialSymbolStack,
    rhs: PartialSymbolStack,
    lhs_suffix_symbols: tuple[PartialScopedSymbol, ...],
    bindings: _SymbolUnifyBindings,
) -> PartialSymbolStack:
    rhs_var = rhs.variable
    if rhs_var is None:
        _raise_symbol_stack_unsatisfied()
    if lhs.variable is not None and lhs.variable == rhs_var:
        _raise_symbol_stack_unsatisfied()
    bindings.symbol_bindings.add(
        rhs_var,
        PartialSymbolStack(symbols=lhs_suffix_symbols, variable=lhs.variable),
        bindings.scope_bindings,
    )
    return PartialSymbolStack(symbols=prefix + lhs_suffix_symbols, variable=lhs.variable)


def _unify_symbol_lhs_is_prefix_of_rhs(
    prefix: tuple[PartialScopedSymbol, ...],
    lhs: PartialSymbolStack,
    rhs: PartialSymbolStack,
    rhs_suffix_symbols: tuple[PartialScopedSymbol, ...],
    bindings: _SymbolUnifyBindings,
) -> PartialSymbolStack:
    lhs_var = lhs.variable
    if lhs_var is None:
        _raise_symbol_stack_unsatisfied()
    if rhs.variable is not None and rhs.variable == lhs_var:
        _raise_symbol_stack_unsatisfied()
    bindings.symbol_bindings.add(
        lhs_var,
        PartialSymbolStack(symbols=rhs_suffix_symbols, variable=rhs.variable),
        bindings.scope_bindings,
    )
    return PartialSymbolStack(symbols=prefix + rhs_suffix_symbols, variable=rhs.variable)
