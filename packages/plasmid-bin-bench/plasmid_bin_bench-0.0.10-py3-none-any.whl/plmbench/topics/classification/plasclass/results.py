"""PlasClass results."""

from __future__ import annotations

from pathlib import Path
from typing import final

from slurmbench.prelude.tool import results as core


@final
class PlasmidProbabilities(core.Result):
    """Plasmid probabilities result."""

    TSV_NAME = Path("plasmid_probabilities.tsv")

    @classmethod
    def _tsv_builder(cls, directory: Path) -> Path:
        return directory / cls.TSV_NAME

    def tsv(self, sample: core.Sample) -> Path:
        """Get plasmid probabilities TSV file."""
        return self._tsv_builder(self.exp_fs_manager().sample_dir(sample))

    def tsv_sh_var(self) -> Path:
        """Get plasmid probabilities TSV file when sample name is a sh variable."""
        return self._tsv_builder(self.exp_fs_manager().sample_sh_var_dir())
