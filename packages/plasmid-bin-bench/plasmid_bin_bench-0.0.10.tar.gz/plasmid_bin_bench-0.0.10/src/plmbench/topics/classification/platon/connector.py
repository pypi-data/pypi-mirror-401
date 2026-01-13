"""Platon connector module."""

from __future__ import annotations

from typing import cast, final

from slurmbench.prelude.tool import connector as core

import plmbench.topics.assembly.results as asm_res
import plmbench.topics.assembly.visitor as asm_visitor

from . import shell as sh


@final
class GenomeArg(
    core.ShExpArg[asm_visitor.Tools, asm_res.FastaGZ, sh.GenomeInputLinesBuilder],
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
    def sh_lines_builder_type(cls) -> type[sh.GenomeInputLinesBuilder]:
        """Get shell lines builder type."""
        return sh.GenomeInputLinesBuilder


@final
class Arguments(core.Arguments):
    """Platon arguments."""

    KEY_GENOME = "GENOME"

    @classmethod
    def node_name_types(cls) -> dict[str, type[core.AnyArg | core.AnyNodeContainer]]:
        """Get list of arg types."""
        return {
            cls.KEY_GENOME: GenomeArg,
        }

    def genome_arg(self) -> GenomeArg:
        """Get genome arg."""
        return cast("GenomeArg", self.__arguments[self.KEY_GENOME])


@final
class Connector(core.WithArguments[Arguments]):
    """Platon connector."""

    @classmethod
    def arguments_type(cls) -> type[Arguments]:
        """Get arguments type."""
        return Arguments
