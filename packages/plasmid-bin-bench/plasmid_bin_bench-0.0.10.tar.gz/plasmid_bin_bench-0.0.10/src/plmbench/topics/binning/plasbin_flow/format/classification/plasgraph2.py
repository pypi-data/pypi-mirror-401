"""PlasBin-flow result formatting module."""

import pandas as pd
from slurmbench.prelude.tool import results as core

import plmbench.topics.assembly.visitor as asm_visitor
import plmbench.topics.classification.plasgraph2.results as plasgraph2_res
from plmbench.topics.classification.plasgraph2 import connector

from . import ops, results


def plasmidness(
    plasgraph2_data_exp_fs_manager: core.ExpFSDataManager,
    sample: core.Sample,
) -> results.Plasmidness:
    """Convert Platon result into plasmidness PlasBin-flow input."""
    plm_prob_res = plasgraph2_res.PlasmidProbabilities(
        plasgraph2_data_exp_fs_manager,
    )
    pbf_plasmidness_res = results.Plasmidness(
        plasgraph2_data_exp_fs_manager,
    )

    plasgraph2_gfa_arg = (
        core.connector_from_exp_fs_data_manager(
            connector.Connector,
            plasgraph2_data_exp_fs_manager,
        )
        .arguments()
        .gfa_arg()
    )

    asm_data_fs_manager = core.ExpFSDataManager(
        plasgraph2_data_exp_fs_manager.root_dir(),
        asm_visitor.Tools(plasgraph2_gfa_arg.tool()).to_description(),
        plasgraph2_gfa_arg.experiment_name(),
    )
    gfa_gz = (
        plasgraph2_gfa_arg.result_visitor()
        .result_builder()(asm_data_fs_manager)
        .gfa_gz(sample)
    )

    plgr_df = pd.read_csv(plm_prob_res.csv(sample))
    contigs_dict = ops.parse_gfa(gfa_gz, plasgraph2_gfa_arg.tool())
    for _, row in plgr_df.iterrows():
        contig_id = str(row["contig"]).split(" ")[0]
        prcr, prpl = row["chrom_score"], row["plasmid_score"]
        pred = row["label"]
        if contig_id in contigs_dict:
            contigs_dict[contig_id]["Prob_Chromosome"] = float(prcr)
            contigs_dict[contig_id]["Prob_Plasmid"] = float(prpl)
            if pred == "plasmid":
                contigs_dict[contig_id]["Prediction"] = "Plasmid"
            else:
                contigs_dict[contig_id]["Prediction"] = "Chromosome"
    contigs_df = pd.DataFrame.from_dict(contigs_dict).T

    contigs_df.to_csv(
        pbf_plasmidness_res.tsv(sample),
        columns=["Prob_Plasmid"],
        sep="\t",
        header=False,
        index=True,
    )

    return pbf_plasmidness_res


def seeds(
    plasgraph2_data_exp_fs_manager: core.ExpFSDataManager,
    sample: core.Sample,
) -> results.Seeds:
    """Convert plasmid stats to PBF format."""
    plm_prob_res = plasgraph2_res.PlasmidProbabilities(
        plasgraph2_data_exp_fs_manager,
    )
    pbf_seeds_res = results.Seeds(
        plasgraph2_data_exp_fs_manager,
    )

    plasgraph2_gfa_arg = (
        core.connector_from_exp_fs_data_manager(
            connector.Connector,
            plasgraph2_data_exp_fs_manager,
        )
        .arguments()
        .gfa_arg()
    )

    asm_data_fs_manager = core.ExpFSDataManager(
        plasgraph2_data_exp_fs_manager.root_dir(),
        asm_visitor.Tools(plasgraph2_gfa_arg.tool()).to_description(),
        plasgraph2_gfa_arg.experiment_name(),
    )
    gfa_gz = (
        plasgraph2_gfa_arg.result_visitor()
        .result_builder()(asm_data_fs_manager)
        .gfa_gz(sample)
    )

    seed_contigs: list[str] = []

    plgr_df = pd.read_csv(plm_prob_res.csv(sample))
    contigs_dict = ops.parse_gfa(gfa_gz, plasgraph2_gfa_arg.tool())
    for _, row in plgr_df.iterrows():
        contig_id = str(row["contig"]).split(" ")[0]
        pred = row["label"]
        if contig_id in contigs_dict and pred == "plasmid":
            seed_contigs.append(contig_id)

    with pbf_seeds_res.tsv(sample).open("w") as f:
        for contig_id in seed_contigs:
            f.write(f"{contig_id}\n")

    return pbf_seeds_res
