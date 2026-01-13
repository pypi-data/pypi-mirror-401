"""PlasClass description."""

from slurmbench.prelude.tool import description as core

import plmbench.topics.classification.description as class_desc

DESCRIPTION = core.Description(
    "PLASCLASS",
    "plasclass",
    class_desc.DESCRIPTION,
)
