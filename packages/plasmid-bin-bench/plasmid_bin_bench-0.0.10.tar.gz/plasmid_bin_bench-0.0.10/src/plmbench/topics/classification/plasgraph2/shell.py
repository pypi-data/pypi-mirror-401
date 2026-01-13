"""plASgraph2 Bash script logics."""

from collections.abc import Iterator
from typing import final

from slurmbench.prelude.tool import bash as core

import plmbench.topics.assembly.results as asm_res
import plmbench.topics.classification.plasgraph2.results as plasgraphtwo_res


@final
class GFAInputLinesBuilder(core.ExpArg[asm_res.AsmGraphGZ]):
    """GFA input bash lines builder."""

    GFA_GZ_VAR = core.BashVar("GFA")

    OUTFILE_VAR = core.BashVar("OUTFILE")

    def init_lines(self) -> Iterator[str]:
        """Get shell input init lines."""
        yield self.GFA_GZ_VAR.set_path(self.input_result().gfa_gz_sh_var())
        yield self.OUTFILE_VAR.set_path(
            plasgraphtwo_res.PlasmidProbabilities(
                self.work_exp_fs_manager(),
            ).csv_sh_var(),
        )
