"""PlasClass connector module."""

from __future__ import annotations

from typing import cast, final

from slurmbench.prelude.tool import connector as core

import plmbench.topics.assembly.results as asm_res
import plmbench.topics.assembly.visitor as asm_visitor

from . import bash as sh


@final
class FASTAArg(
    core.ShExpArg[asm_visitor.Tools, asm_res.FastaGZ, sh.FastaInputLinesBuilder],
):
    """Genome argument."""

    @classmethod
    def tools_type(cls) -> type[asm_visitor.Tools]:
        """Get tools type."""
        return asm_visitor.Tools

    @classmethod
    def result_visitor(cls) -> type[asm_res.FastaGZVisitor]:
        """Get result visitor."""
        return asm_res.FastaGZVisitor

    @classmethod
    def sh_lines_builder_type(cls) -> type[sh.FastaInputLinesBuilder]:
        """Get shell lines builder type."""
        return sh.FastaInputLinesBuilder


@final
class Arguments(core.Arguments):
    """Platon arguments."""

    KEY_FASTA = "FASTA"

    @classmethod
    def node_name_types(cls) -> dict[str, type[core.AnyArg | core.AnyNodeContainer]]:
        """Get list of arg types."""
        return {
            cls.KEY_FASTA: FASTAArg,
        }

    def fasta_arg(self) -> FASTAArg:
        """Get FASTA argument."""
        return cast("FASTAArg", self.__arguments[self.KEY_FASTA])


@final
class Connector(core.WithArguments[Arguments]):
    """Platon connector."""

    @classmethod
    def arguments_type(cls) -> type[Arguments]:
        """Get arguments type."""
        return Arguments
