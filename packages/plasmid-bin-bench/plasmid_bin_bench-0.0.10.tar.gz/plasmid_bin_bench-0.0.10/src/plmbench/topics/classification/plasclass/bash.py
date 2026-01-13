"""Platon Bash script logics."""

from collections.abc import Iterator
from pathlib import Path
from typing import final

from slurmbench.prelude.tool import bash as core

import plmbench.topics.assembly.results as asm_res
import plmbench.topics.classification.plasclass.results as plasclass_res


@final
class FastaInputLinesBuilder(core.ExpArg[asm_res.FastaGZ]):
    """Fasta input bash lines builder."""

    FASTA_GZ_VAR = core.BashVar("FASTA_GZ")

    FASTA_VAR = core.BashVar("FASTA")
    OUTFILE_VAR = core.BashVar("OUTFILE")

    def __fasta_tmp_file(self) -> Path:
        """Return a tmp FASTA path with sample name is a sh variable."""
        return self.input_result().fasta_gz_sh_var().with_suffix("")

    def init_lines(self) -> Iterator[str]:
        """Get shell input init lines."""
        yield self.FASTA_GZ_VAR.set_path(self.input_result().fasta_gz_sh_var())
        yield self.FASTA_VAR.set_path(self.__fasta_tmp_file())
        yield self.OUTFILE_VAR.set_path(
            plasclass_res.PlasmidProbabilities(self.work_exp_fs_manager()).tsv_sh_var(),
        )
