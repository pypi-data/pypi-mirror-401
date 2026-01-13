"""Concrete tool connector module."""

from __future__ import annotations

from typing import cast, final

from slurmbench.prelude.tool import connector as core

import plmbench.topics.assembly.results as asm_res
import plmbench.topics.assembly.visitor as asm_visitor
import plmbench.topics.classification.visitor as class_visitor
from plmbench.topics.binning.plasbin_flow.format.classification import (
    results as fmt_class_res,
)
from plmbench.topics.binning.plasbin_flow.format.classification import (
    visitor as fmt_class_visitor,
)

from . import shell as sh


@final
class GFAArg(core.ExpArg[asm_visitor.Tools, asm_res.AsmGraphGZ]):
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
class SeedsArg(core.ExpArg[class_visitor.Tools, fmt_class_res.Seeds]):
    """Seeds argument."""

    @classmethod
    def tools_type(cls) -> type[class_visitor.Tools]:
        """Get tools type."""
        return class_visitor.Tools

    @classmethod
    def result_visitor(cls) -> type[fmt_class_visitor.SeedsVisitor]:
        """Get result visitor."""
        return fmt_class_visitor.SeedsVisitor

    @classmethod
    def sh_lines_builder_type(cls) -> type[sh.SeedsInputLinesBuilder]:
        """Get shell lines builder type."""
        return sh.SeedsInputLinesBuilder


@final
class PlasmidnessArg(core.ExpArg[class_visitor.Tools, fmt_class_res.Plasmidness]):
    """Plasmidness argument."""

    @classmethod
    def tools_type(cls) -> type[class_visitor.Tools]:
        """Get tools type."""
        return class_visitor.Tools

    @classmethod
    def result_visitor(cls) -> type[fmt_class_visitor.PlasmidnessVisitor]:
        """Get result visitor."""
        return fmt_class_visitor.PlasmidnessVisitor

    @classmethod
    def sh_lines_builder_type(
        cls,
    ) -> type[sh.PlasmidnessInputLinesBuilder]:
        """Get shell lines builder type."""
        return sh.PlasmidnessInputLinesBuilder


@final
class Arguments(core.Arguments):
    """Concrete tool arguments."""

    KEY_GFA = "GFA"
    KEY_SEEDS = "SEEDS"
    KEY_PLASMIDNESS = "PLASMIDNESS"

    @classmethod
    def node_name_types(cls) -> dict[str, type[core.AnyArg | core.AnyNodeContainer]]:
        """Get list of arg types."""
        return {
            cls.KEY_GFA: GFAArg,
            cls.KEY_SEEDS: SeedsArg,
            cls.KEY_PLASMIDNESS: PlasmidnessArg,
        }

    def gfa_arg(self) -> GFAArg:
        """Get GFA argument."""
        return cast("GFAArg", self.__arguments[self.KEY_GFA])

    def seeds_arg(self) -> SeedsArg:
        """Get seeds argument."""
        return cast("SeedsArg", self.__arguments[self.KEY_SEEDS])

    def plasmidness_arg(self) -> PlasmidnessArg:
        """Get plasmidness argument."""
        return cast("PlasmidnessArg", self.__arguments[self.KEY_PLASMIDNESS])


@final
class Connector(core.WithArguments[Arguments]):
    """Concrete tool connector."""

    @classmethod
    def arguments_type(cls) -> type[Arguments]:
        """Get arguments type."""
        return Arguments
