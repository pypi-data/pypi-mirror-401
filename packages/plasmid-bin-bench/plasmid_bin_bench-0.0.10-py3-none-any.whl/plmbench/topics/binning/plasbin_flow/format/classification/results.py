"""PlasBin-flow classification result formatting module."""

from pathlib import Path
from typing import final

from slurmbench.prelude.tool import results as core


@final
class Plasmidness(core.Result):
    """Plasmidness PlasBin-flow formatted result."""

    TSV_NAME = Path("pbf_plasmidness.tsv")

    @classmethod
    def _tsv_builder(cls, directory: Path) -> Path:
        return directory / cls.TSV_NAME

    def tsv(self, sample: core.Sample) -> Path:
        """Get plasmidness TSV file."""
        return self._tsv_builder(self.exp_fs_manager().sample_dir(sample))

    def tsv_sh_var(self) -> Path:
        """Get plasmidness TSV file when sample name is a sh variable."""
        return self._tsv_builder(self.exp_fs_manager().sample_sh_var_dir())


@final
class Seeds(core.Result):
    """Seeds PlasBin-flow formatted result."""

    TSV_NAME = Path("pbf_seeds.tsv")

    @classmethod
    def _tsv_builder(cls, directory: Path) -> Path:
        return directory / cls.TSV_NAME

    def tsv(self, sample: core.Sample) -> Path:
        """Get seeds TSV file."""
        return self._tsv_builder(self.exp_fs_manager().sample_dir(sample))

    def tsv_sh_var(self) -> Path:
        """Get seeds TSV file when sample name is a sh variable."""
        return self._tsv_builder(self.exp_fs_manager().sample_sh_var_dir())
