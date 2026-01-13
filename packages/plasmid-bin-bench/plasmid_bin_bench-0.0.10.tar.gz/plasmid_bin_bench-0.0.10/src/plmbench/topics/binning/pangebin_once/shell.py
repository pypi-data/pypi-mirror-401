"""Concrete tool Bash script logics."""

from collections.abc import Iterator
from typing import final

from slurmbench.prelude.tool import bash as core

import plmbench.topics.assembly.results as asm_res
from plmbench.topics.binning.plasbin_flow.format.classification import (
    results as fmt_class_res,
)


@final
class GFAInputLinesBuilder(core.ExpArg[asm_res.AsmGraphGZ]):
    """GFA input bash lines builder."""

    GFA_GZ_VAR = core.BashVar("GFA")

    def init_lines(self) -> Iterator[str]:
        """Get shell input init lines."""
        yield self.GFA_GZ_VAR.set_path(self.input_result().gfa_gz_sh_var())


@final
class SeedsInputLinesBuilder(core.ExpArg[fmt_class_res.Seeds]):
    """Seeds input bash lines builder."""

    SEEDS_VAR = core.BashVar("SEEDS")

    def init_lines(self) -> Iterator[str]:
        """Get shell input init lines."""
        yield self.SEEDS_VAR.set_path(self.input_result().tsv_sh_var())

    def close_lines(self) -> Iterator[str]:
        """Get shell input close lines."""
        yield from ()


@final
class PlasmidnessInputLinesBuilder(core.ExpArg[fmt_class_res.Plasmidness]):
    """Plasmidness input bash lines builder."""

    PLASMIDNESS_VAR = core.BashVar("PLASMIDNESS")

    def init_lines(self) -> Iterator[str]:
        """Get shell input init lines."""
        yield self.PLASMIDNESS_VAR.set_path(self.input_result().tsv_sh_var())
