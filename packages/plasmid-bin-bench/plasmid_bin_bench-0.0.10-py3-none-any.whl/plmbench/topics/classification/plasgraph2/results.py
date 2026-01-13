"""plASgraph2 results."""

from __future__ import annotations

from pathlib import Path
from typing import final

from slurmbench.prelude.tool import results as core


@final
class PlasmidProbabilities(core.Result):
    """Plasmid probabilities result."""

    CSV_NAME = Path("plasmid_probabilities.csv")

    @classmethod
    def _csv_builder(cls, directory: Path) -> Path:
        return directory / cls.CSV_NAME

    def csv(self, sample: core.Sample) -> Path:
        """Get plasmid probabilities CSV file."""
        return self._csv_builder(self.exp_fs_manager().sample_dir(sample))

    def csv_sh_var(self) -> Path:
        """Get plasmid probabilities CSV file when sample name is a sh variable."""
        return self._csv_builder(self.exp_fs_manager().sample_sh_var_dir())
