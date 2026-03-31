#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import sys

import click_completion
import rich_click as click
from sequana_pipetools import SequanaManager
from sequana_pipetools.options import *

click_completion.init()
NAME = "bioconvert"


help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--input-ext",
            "--output-ext",
            "--command",
            "--method",
        ],
    },
)


from bioconvert import logger as blog

# retrieve possible commands from the bioconvert registry.
from bioconvert.core.registry import Registry

blog.level = "ERROR"
r = Registry()
blog.level = "WARNING"
commands = list(r.get_converters_names())


@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--input-pattern",
    "input_pattern",
    default="*",
    show_default=True,
    type=click.STRING,
    help="""Prefix glob pattern to restrict which files are picked up. Combined with
        --input-ext to form the actual file pattern (e.g. '*' + 'fastq.gz' → '*.fastq.gz').
        Useful when only a subset of files in the directory should be converted.""",
)
@click.option(
    "--input-directory",
    "input_directory",
    required=True,
    type=click.Path(dir_okay=True, file_okay=False),
    help="""The input directory where to look for input files""",
)
@click.option(
    "--input-ext",
    "input_extension",
    required=True,
    type=click.STRING,
    help="""The extension of the files to convert. See bioconvert --help for details""",
)
@click.option(
    "--output-ext",
    "output_extension",
    required=True,
    type=click.STRING,
    help="""The extension of the output files. See bioconvert --help for details""",
)
@click.option(
    "--command",
    "command",
    required=True,
    type=click.Choice(commands),
    help="""One of the possible conversion available in bioconvert.""",
)
@click.option(
    "--method",
    "method",
    type=click.STRING,
    default=None,
    help="Override the default conversion method for the chosen command. "
    "Run 'bioconvert COMMAND --show-methods' to list valid methods.",
)
def main(**options):
    """

    To convert a set of fastq.gz files into fasta.gz, run:

        sequana_bioconvert --input-directory data/ --input-ext fastq.gz --output-ext fasta.gz
            --command fastq2fasta

        cd bioconvert
        sh bioconvert.sh

    Use --input-pattern to restrict conversion to a subset of files, e.g. --input-pattern "sample_*".
    Use --method to override the default conversion method, e.g. --method pysam.

    """

    if options["from_project"]:
        click.echo("--from-project Not yet implemented")
        sys.exit(1)

    # the real stuff is here
    manager = SequanaManager(options, NAME)
    manager.setup()

    # aliases
    options = manager.options
    cfg = manager.config.config

    from sequana_pipetools import logger

    logger.setLevel(options.level)

    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.input_pattern = options.input_pattern + "." + options.input_extension
    cfg.bioconvert.method = options.method or ""
    cfg.bioconvert.command = options.command
    cfg.bioconvert.input_extension = options.input_extension
    cfg.bioconvert.output_extension = options.output_extension

    manager.exists(cfg.input_directory)

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
