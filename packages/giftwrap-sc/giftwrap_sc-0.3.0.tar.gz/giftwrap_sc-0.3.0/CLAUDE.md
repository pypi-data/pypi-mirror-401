# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GIFTwrap is a Python package for processing and analyzing GIFT-seq (Gapfill-based Integrated Functional Targeted sequencing) data. It provides both a CLI pipeline for converting FASTQ files to count matrices and a Python API for downstream analysis, particularly focused on single-cell and spatial transcriptomics with targeted variant detection.

**Key concepts:**
- GIFT-seq uses probe-based gapfilling to detect specific genetic variants (e.g., SNVs) in single cells
- The pipeline processes paired-end FASTQ files containing both WTA (whole transcriptome) and gapfill probes
- Features in output files are NOT single genes/probes but unique combinations of probes and gapfill products
- Multiple data matrices are generated: counts, total_reads (including PCR duplicates), and percent_supporting

## Development Commands

### Environment Setup
```bash
# Install dependencies (requires uv: https://docs.astral.sh/uv/)
uv sync --all-extras --all-groups

# Build package
uv build

# Publish (maintainers only)
uv publish --token <your-pypi-token>
```

### Documentation
```bash
# Preview documentation locally
uv run mkdocs serve
# Opens at http://localhost:8000

# Documentation auto-deploys via GitHub Actions on commit
```

### Testing the Pipeline
The basic pipeline command processes FASTQ files:
```bash
# All-in-one command
giftwrap --probes path/to/probes.xlsx --project fastqs/fastq_prefix -o output_dir/

# With WTA data for filtering
giftwrap --probes probes.xlsx --project fastqs/prefix -wta filtered_feature_bc_matrix.h5 -o output/

# Individual steps (for debugging or custom workflows)
giftwrap-count        # Step 1: Parse FASTQs and count gapfills
giftwrap-correct-umis # Step 2: Correct UMI sequencing errors
giftwrap-correct-gapfill # Step 3: Correct gapfill sequencing errors
giftwrap-collect      # Step 4: Aggregate counts into matrices
giftwrap-summarize    # Step 5: Generate summary statistics and plots
```

## Architecture

### Pipeline Structure (5-step processing)

The CLI pipeline follows a sequential 5-step architecture implemented in separate modules:

1. **step1_count_gapfills.py**: Parses FASTQ files, corrects cell barcodes and probe sequences using error-tolerant matching, and extracts gapfill sequences
2. **step2_correct_umis.py**: Performs UMI deduplication and error correction
3. **step3_correct_gapfill.py**: Corrects gapfill sequences against expected variants
4. **step4_collect_counts.py**: Aggregates corrected reads into Cell×Feature sparse matrices
5. **step5_summarize_counts.py**: Generates QC metrics (fastq_metrics.tsv, counts.N.summary.csv) and visualization (counts.N.summary.pdf)

**Important**: The `pipeline.py` orchestrates these steps by calling each as a subprocess. Each step can also be run independently for debugging or custom workflows.

### Core Modules

- **utils.py**: Central utilities including:
  - `TechnologyFormatInfo`: Abstract base class for technology-specific parsing (Flex, VisiumHD, Visium)
  - `ProbeParser`: Error-tolerant probe sequence matching using prefix tries
  - `read_h5_file()`: Loads count matrices into AnnData objects
  - `maybe_multiprocess()`: Multiprocessing abstraction for single/multi-core execution

- **analysis/**: Python API for downstream analysis (namespace: `gw.pp`, `gw.tl`, `gw.pl`, `gw.sp`)
  - **preprocess.py** (`gw.pp`): Data filtering (e.g., `filter_gapfills()`)
  - **tools.py** (`gw.tl`): Core analysis (genotype calling, collapsing features, WTA integration)
  - **plots.py** (`gw.pl`): Visualization (dendrograms, matrixplots, UMAPs)
  - **spatial.py** (`gw.sp`): Spatial data integration with spatialdata

### Technology Definitions

The package supports multiple spatial transcriptomics platforms through the `TechnologyFormatInfo` abstraction:
- **FlexFormatInfo**: 10x Genomics Flex (default)
- **VisiumHDFormatInfo**: Visium HD with protobuf-based barcode parsing
- **VisiumFormatInfo**: Standard Visium

Custom technologies can be defined by subclassing `TechnologyFormatInfo` and generated via:
```bash
giftwrap-generate-tech > tech_def.py  # Get template
giftwrap --technology Custom --tech_def tech_def.py ...  # Use custom definition
```

Barcode whitelists and coordinates are stored in `src/giftwrap/resources/` (e.g., visium-v5.txt, chemistry_defs.json).

### Data Flow

```
FASTQ files (R1: cell barcode/UMI, R2: probes/gapfill)
    ↓ step1_count_gapfills.py
Parsed reads (TSV with cell, UMI, probe, gapfill)
    ↓ step2_correct_umis.py
UMI-deduplicated reads
    ↓ step3_correct_gapfill.py
Corrected gapfills (matched to expected variants)
    ↓ step4_collect_counts.py
HDF5 matrices (counts.N.h5, counts.N.filtered.h5)
    ↓ step5_summarize_counts.py (or Python API)
QC reports + Analysis (genotype calling, spatial integration)
```

### Output File Structure

- `manifest.tsv`: Probe metadata (name, lhs_probe, rhs_probe, expected gapfills)
- `fastq_metrics.tsv`: Read-level statistics (total reads, correction rates, filtering reasons)
- `counts.N.h5`: Unfiltered count matrix (all cell barcodes)
- `counts.N.filtered.h5`: Filtered matrix (only valid cells from WTA if provided)
- `counts.N.summary.csv`: Cell-level statistics (UMIs per cell, gapfills per probe)
- `counts.N.summary.pdf`: QC visualizations

## Important Implementation Details

### Error Correction Strategy
- Cell barcodes, probe sequences, and gapfills all use Hamming distance-based correction
- Maximum edit distance is configurable via `--max-distance` (default: 1)
- Uses prefix tries for efficient approximate matching of probe sequences
- Multiprocessing support via `maybe_multiprocess()` which handles both single-core (fallback to itertools) and multi-core (multiprocessing.Pool) execution

### Probe File Format
Input probe files (.tsv, .csv, .xlsx) must contain:
- `name` (required): Convention is "gene_name HGVSc" (e.g., "TP53 c.215G>A")
- `lhs_probe` (required): Left-hand side probe sequence
- `rhs_probe` (required): Right-hand side probe sequence
- `gap_probe_sequence` (optional): Expected gapfill for variant
- `original_gap_probe_sequence` (optional): Expected WT gapfill for SNV analysis
- `gene` (optional): Gene name (defaults to first word of `name`)

### HDF5 Data Structure
The output .h5 files contain:
- Three sparse matrices: `counts`, `total_reads`, `percent_supporting`
- Feature metadata: `probe_id`, `probe_name`, `gapfill_sequence`, `gene`
- Cell barcode list and optional spatial coordinates (X, Y)
- Compatible with scanpy/AnnData and Seurat (via provided R script)

### Python API Usage Patterns

Typical analysis workflow:
```python
import giftwrap as gw
import scanpy as sc

# Load data
gapfill_adata = gw.read_h5_file("counts.1.filtered.h5")
wta_adata = sc.read_10x_h5("filtered_feature_bc_matrix.h5")

# Preprocessing
gw.pp.filter_gapfills(gapfill_adata)  # Remove low-quality genotypes
wta_adata, gapfill_adata = gw.tl.intersect_wta(wta_adata, gapfill_adata)

# Analysis
gw.tl.call_genotypes(gapfill_adata)  # Assign discrete genotype calls
gw.tl.transfer_genotypes(wta_adata, gapfill_adata)  # Transfer to WTA for UMAP

# Visualization
gw.pl.matrixplot(gapfill_adata, "TP53 c.215G>A", "celltype")
gw.pl.umap(wta_adata, "TP53 c.215G>A")  # Plot on WTA UMAP

# Spatial analysis (requires [spatial] extras)
import spatialdata as sd
wta_spatial = sd.read_visium(...)
wta_spatial = gw.sp.join_with_wta(wta_spatial, gapfill_adata)
```

## Common Patterns and Conventions

- Multiprocessing is memory-intensive for VisiumHD due to high barcode complexity
- Always use WTA data (`-wta` flag) for cell calling when available—gapfill-only calling is noisy
- When working with spatial data, install the `[spatial]` or `[all]` extras
- The package patches numpy for compatibility: `np.float_ = np.float64`, `np.infty = np.inf`
- Future warnings are suppressed globally to reduce noise from dependencies

## Documentation Structure

Documentation is in `docs/` and built with mkdocs-material:
- `tutorials/`: Getting started, processing, analysis, spatial, imputation, Seurat integration
- `cli/`: Full reference for all CLI commands
- `api/`: Auto-generated from docstrings (Sphinx style)
- `file_formats.md`: Detailed specification of probe files and output formats
