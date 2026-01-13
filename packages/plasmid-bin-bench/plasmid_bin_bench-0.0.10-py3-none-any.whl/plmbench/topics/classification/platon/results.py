"""Tool results."""

from __future__ import annotations

from typing import TYPE_CHECKING, final

from slurmbench.prelude.tool import results as core

import plmbench.topics.assembly.results as asm_res

if TYPE_CHECKING:
    from pathlib import Path


@final
class PlasmidStats(core.Result):
    """Plasmid stats result."""

    # TSV name: "assembly.tsv"
    # * no `.fasta` because Platon removes the extension
    # * no `.gz` because Platon takes an not-compressed FASTA file
    TSV_NAME = asm_res.FastaGZ.FASTA_GZ_NAME.with_suffix("").with_suffix(".tsv")

    @classmethod
    def _tsv_builder(cls, directory: Path) -> Path:
        return directory / cls.TSV_NAME

    def tsv(self, sample: core.Sample) -> Path:
        """Get TSV file."""
        return self._tsv_builder(self.exp_fs_manager().sample_dir(sample))

    def tsv_sh_var(self) -> Path:
        """Get TSV file when sample name is a sh variable."""
        return self._tsv_builder(self.exp_fs_manager().sample_sh_var_dir())
