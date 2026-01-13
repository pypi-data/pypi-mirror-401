"""PlasBin-flow result formatting module."""

import gzip

import pandas as pd
from Bio import SeqIO
from slurmbench.prelude.tool import results as core

import plmbench.topics.assembly.visitor as asm_visitor
import plmbench.topics.classification.platon.results as platon_res
from plmbench.topics.classification.platon import connector

from . import results


def plasmidness(
    platon_data_exp_fs_manager: core.ExpFSDataManager,
    sample: core.Sample,
) -> results.Plasmidness:
    """Convert Platon result into plasmidness PlasBin-flow input."""
    plasmidness_res = platon_res.PlasmidStats(platon_data_exp_fs_manager)
    pbf_plasmidness_res = results.Plasmidness(
        platon_data_exp_fs_manager,
    )
    match platon_connector := connector.Connector.from_yaml(
        platon_data_exp_fs_manager.config_yaml(),
    ):
        case core.ConnectorError():
            raise ValueError(platon_connector.error())

    platon_genome_arg = (
        core.connector_from_exp_fs_data_manager(
            connector.Connector,
            platon_data_exp_fs_manager,
        )
        .arguments()
        .genome_arg()
    )

    asm_data_fs_manager = core.ExpFSDataManager(
        platon_data_exp_fs_manager.root_dir(),
        asm_visitor.Tools(platon_genome_arg.tool()).to_description(),
        platon_genome_arg.experiment_name(),
    )
    fasta_gz = (
        platon_genome_arg.result_visitor()
        .result_builder()(asm_data_fs_manager)
        .fasta_gz(sample)
    )

    with plasmidness_res.tsv(sample).open() as tsv_file:
        set_of_platon_ids = {line.split("\t")[0] for line in tsv_file}

    with (
        pbf_plasmidness_res.tsv(sample).open("w") as tsv_file,
        gzip.open(fasta_gz, "rt") as fasta_gz_file,
    ):
        for record in SeqIO.parse(fasta_gz_file, "fasta"):  # type: ignore[no-untyped-call]
            if record.name in set_of_platon_ids:
                tsv_file.write(f"{record.name}\t1\n")
            else:
                tsv_file.write(f"{record.name}\t0\n")

    return pbf_plasmidness_res


def seeds(
    platon_data_exp_fs_manager: core.ExpFSDataManager,
    sample: core.Sample,
) -> results.Seeds:
    """Convert plasmid stats to PBF format."""
    seeds_res = platon_res.PlasmidStats(platon_data_exp_fs_manager)
    pbf_seeds_res = results.Seeds(
        platon_data_exp_fs_manager,
    )

    platon_seeds_stats_df = pd.read_csv(
        seeds_res.tsv(sample),
        sep="\t",
    )

    platon_seeds_stats_df.to_csv(
        pbf_seeds_res.tsv(sample),
        columns=["ID"],
        header=False,
        sep="\t",
        index=False,
    )
    return pbf_seeds_res
