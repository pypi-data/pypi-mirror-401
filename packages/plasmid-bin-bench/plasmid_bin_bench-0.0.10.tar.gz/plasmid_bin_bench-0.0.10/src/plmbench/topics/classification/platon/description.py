"""Platon description module."""

from slurmbench.prelude.tool import description as core

import plmbench.topics.classification.description as class_desc

DESCRIPTION = core.Description("PLATON", "platon", class_desc.DESCRIPTION)
