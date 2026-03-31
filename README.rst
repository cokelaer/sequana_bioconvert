
.. image:: https://badge.fury.io/py/sequana-bioconvert.svg
     :target: https://pypi.python.org/pypi/sequana_bioconvert

.. image:: https://github.com/sequana/bioconvert/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/bioconvert/actions/workflows/main.yml

.. image:: https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg
    :target: https://pypi.python.org/pypi/sequana_bioconvert
    :alt: Python 3.10 | 3.11 | 3.12

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI


bioconvert — format conversion pipeline
========================================

:Overview: Parallelise `bioconvert <https://bioconvert.readthedocs.io>`_ conversions across a set of files
:Input: Any file format supported by bioconvert (FastQ, BAM, FASTA, VCF, …)
:Output: Converted files in the target format, MD5 checksums, and an HTML summary report
:Status: Production
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines,
           Journal of Open Source Software, 2(16), 352,
           `doi:10.21105/joss.00352 <https://doi.org/10.21105/joss.00352>`_

.. image:: https://raw.githubusercontent.com/sequana/bioconvert/main/sequana_pipelines/bioconvert/dag.png
   :alt: Pipeline DAG


Installation
------------

::

    pip install sequana-bioconvert

To upgrade an existing installation::

    pip install sequana-bioconvert --upgrade

Install all dependencies via conda/mamba::

    mamba env create -f environment.yml


Quick Start
-----------

**Step 1 — prepare the working directory**

Convert all ``fastq.gz`` files in a directory to ``fasta.gz``::

    sequana_bioconvert \
        --input-directory /path/to/data \
        --input-ext fastq.gz \
        --output-ext fasta.gz \
        --command fastq2fasta

This creates a ``bioconvert/`` working directory with ``config.yaml`` and a
``bioconvert.sh`` launch script.

**Step 2 — run the pipeline**::

    cd bioconvert
    sh bioconvert.sh

Results are written to the ``output/`` subdirectory. An HTML summary report is
generated on completion.

Usage
-----

::

    sequana_bioconvert --help

Key options:

- ``--input-directory``  — directory containing the input files (required)
- ``--input-ext``        — extension of input files, e.g. ``fastq.gz`` (required)
- ``--output-ext``       — extension of output files, e.g. ``fasta.gz`` (required)
- ``--command``          — bioconvert conversion command, e.g. ``fastq2fasta`` (required);
                          run ``bioconvert --help`` for the full list
- ``--input-pattern``    — prefix glob to restrict which files are picked up (default: ``*``);
                          e.g. ``sample_*`` to process only files starting with ``sample_``
- ``--method``           — override the default conversion method;
                          run ``bioconvert COMMAND --show-methods`` to list valid methods

Usage with apptainer
--------------------

All external tools are available through a pre-built apptainer image. To use
it, add ``--use-apptainer`` when initialising the pipeline::

    sequana_bioconvert \
        --input-directory /path/to/data \
        --input-ext fastq.gz \
        --output-ext fasta.gz \
        --command fastq2fasta \
        --use-apptainer \
        --apptainer-prefix ~/.sequana/apptainers

Then run as usual::

    cd bioconvert
    sh bioconvert.sh


Requirements
------------

- **bioconvert** ≥ 1.1.0 — the underlying conversion tool
- **graphviz** — for pipeline DAG rendering (available via apptainer)

Install dependencies via conda/mamba::

    mamba env create -f environment.yml

Rules and configuration details
--------------------------------

The latest configuration file is available at:
`config.yaml <https://raw.githubusercontent.com/sequana/bioconvert/main/sequana_pipelines/bioconvert/config.yaml>`_

Each rule used in the pipeline has a corresponding section in ``config.yaml``.

Changelog
---------

========= ====================================================================
Version   Description
========= ====================================================================
1.2.0     * Update apptainer image to bioconvert 1.1.0
          * Switch to ``manager.get_shell()`` — no longer uses sequana_wrappers
          * Remove ``sequana_wrappers`` field from config and schema
          * Use ``importlib.metadata`` for version (fixes ``>=x.y.z`` display
            in HTML reports)
          * ``--input-pattern`` now optional (default ``*``); combined with
            ``--input-ext`` to form the actual glob pattern
          * Add ``md5_output.txt`` alongside ``md5_input.txt``
          * Improved HTML report: method display, bioconvert doc link,
            cleaner table labels
          * Early exit with clear error if no input files are found
          * Fix fragile sample name extraction for multi-dot filenames
1.1.0     * Update apptainer image to bioconvert 1.1.0
          * CI: update to Python 3.10/3.11/3.12 and actions/checkout@v4
1.0.0     Uses bioconvert 1.0.0
0.10.0    Add container
0.9.0     Version using new sequana/sequana_pipetools framework
0.8.1     **Working version**
0.8.0     **First release**
========= ====================================================================


Contribute & Code of Conduct
-----------------------------

To contribute to this project, please take a look at the
`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.
