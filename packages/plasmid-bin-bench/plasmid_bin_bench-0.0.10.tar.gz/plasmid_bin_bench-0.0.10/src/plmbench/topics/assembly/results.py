"""Assembly results.

All the assembly tools must have a common set of results.
"""

# ruff: noqa: ERA001

from __future__ import annotations

from pathlib import Path
from typing import final

from slurmbench.prelude.topic import results as core

import plmbench.topics.assembly.visitor as asm_visitor


@final
class FastaGZ(core.Result):
    """FASTA gunzip result."""

    FASTA_GZ_NAME = Path("assembly.fasta.gz")

    @classmethod
    def _fasta_gz_builder(cls, directory: Path) -> Path:
        return directory / cls.FASTA_GZ_NAME

    def fasta_gz(self, sample: core.Sample) -> Path:
        """Get assembly FASTA file."""
        return self._fasta_gz_builder(self.exp_fs_manager().sample_dir(sample))

    def fasta_gz_sh_var(self) -> Path:
        """Get assembly FASTA file when sample name is a sh variable."""
        return self._fasta_gz_builder(self.exp_fs_manager().sample_sh_var_dir())


@final
class AsmGraphGZ(core.Result):
    """Assembly graph (GFA) gunzip result."""

    ASSEMBLY_GFA_GZ_NAME = Path("assembly.gfa.gz")

    @classmethod
    def _gfa_gz_builder(cls, directory: Path) -> Path:
        return directory / cls.ASSEMBLY_GFA_GZ_NAME

    def gfa_gz(self, sample: core.Sample) -> Path:
        """Get assembly GFA file."""
        return self._gfa_gz_builder(self.exp_fs_manager().sample_dir(sample))

    def gfa_gz_sh_var(self) -> Path:
        """Get assembly GFA file when sample name is a sh variable."""
        return self._gfa_gz_builder(self.exp_fs_manager().sample_sh_var_dir())


@final
class FastaGZVisitor(core.OriginalVisitor[asm_visitor.Tools, FastaGZ]):
    """FastaGZ result visitor."""

    @classmethod
    def result_builder(cls) -> type[FastaGZ]:
        """Get result builder."""
        return FastaGZ

    @classmethod
    def result_builder_from_tool(
        cls,
        tool: asm_visitor.Tools,
    ) -> core.Error | type[FastaGZ]:
        """Visit assembly FASTA tool result."""
        match tool:
            case asm_visitor.Tools.UNICYCLER:
                return cls.result_builder()

            # FEATURE: Add SKESA and GFA_CONNECTOR
            # case asm_visitor.Tools.SKESA:
            #     return cls.result_builder()
            # case asm_visitor.Tools.GFA_CONNECTOR:
            #     return cls.result_builder()


@final
class AsmGraphGZVisitor(core.OriginalVisitor[asm_visitor.Tools, AsmGraphGZ]):
    """Assembly graph (GFA) result visitor."""

    @classmethod
    def result_builder(cls) -> type[AsmGraphGZ]:
        """Get result builder."""
        return AsmGraphGZ

    @classmethod
    def result_builder_from_tool(
        cls,
        tool: asm_visitor.Tools,
    ) -> core.Error | type[AsmGraphGZ]:
        """Visit assembly graph (GFA) tool result."""
        match tool:
            case asm_visitor.Tools.UNICYCLER:
                return cls.result_builder()

            # FEATURE: Add SKESA and GFA_CONNECTOR
            # case asm_visitor.Tools.SKESA:
            #     return core.Error(
            #         f"{asm_visitor.Tools.SKESA} tool"
            #         " does not provide a GFA file"
            #         f" but {asm_visitor.Tools.GFA_CONNECTOR} does",
            #     )
            # case asm_visitor.Tools.GFA_CONNECTOR:
            #     return cls.result_builder()
