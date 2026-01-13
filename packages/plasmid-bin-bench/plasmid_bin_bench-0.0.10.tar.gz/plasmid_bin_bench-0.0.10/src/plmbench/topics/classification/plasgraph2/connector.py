"""plASgraph2 connector module."""

from __future__ import annotations

from typing import cast, final

from slurmbench.prelude.tool import connector as core

import plmbench.topics.assembly.results as asm_res
import plmbench.topics.assembly.visitor as asm_visitor

from . import shell as sh


@final
class GFAArg(
    core.ShExpArg[asm_visitor.Tools, asm_res.AsmGraphGZ, sh.GFAInputLinesBuilder],
):
    """GFA argument."""

    @classmethod
    def tools_type(cls) -> type[asm_visitor.Tools]:
        """Get tools type."""
        return asm_visitor.Tools

    @classmethod
    def result_visitor(cls) -> type[asm_res.AsmGraphGZVisitor]:
        """Get result visitor."""
        return asm_res.AsmGraphGZVisitor

    @classmethod
    def sh_lines_builder_type(cls) -> type[sh.GFAInputLinesBuilder]:
        """Get shell lines builder type."""
        return sh.GFAInputLinesBuilder


@final
class Arguments(core.Arguments):
    """Platon arguments."""

    KEY_GFA = "GFA"

    @classmethod
    def node_name_types(cls) -> dict[str, type[core.AnyArg | core.AnyNodeContainer]]:
        """Get list of arg types."""
        return {
            cls.KEY_GFA: GFAArg,
        }

    def gfa_arg(self) -> GFAArg:
        """Get GFA argument."""
        return cast("GFAArg", self.__arguments[self.KEY_GFA])


@final
class Connector(core.WithArguments[Arguments]):
    """Platon connector."""

    @classmethod
    def arguments_type(cls) -> type[Arguments]:
        """Get arguments type."""
        return Arguments
