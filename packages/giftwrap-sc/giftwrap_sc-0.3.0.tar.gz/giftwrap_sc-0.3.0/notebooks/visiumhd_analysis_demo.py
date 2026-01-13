import os
import gc
from pathlib import Path

# Core packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Single-cell and spatial analysis
import anndata as ad
import scanpy as sc
import squidpy as sq
import spatialdata as sd
import spatialdata_io as sio
from spatialdata import polygon_query
from spatialdata.models import ShapesModel
from shapely import Polygon
from geopandas import GeoDataFrame

# GIFTwrap for targeted variant detection
import giftwrap as gw

# Set plotting parameters
plt.rcParams['figure.dpi'] = 150
plt.rcParams['figure.figsize'] = (10, 10)
sc.settings.set_figure_params(dpi=150, facecolor='white')

print("✓ All packages loaded successfully")


# ============================================================================
# SECTION 1: LOADING VISIUMHD DATA WITH SPATIALDATA
# ============================================================================

def load_visiumhd_data(spaceranger_output_dir: str, dataset_id: str = '') -> sd.SpatialData:
    """
    Load VisiumHD data using SpatialData's native reader.

    Best Practices:
    - Use spatialdata_io.visium_hd() for native SpaceRanger outputs
    - Convert to ZARR format for faster I/O on subsequent loads
    - Keep dataset_id empty if you want default naming

    Parameters:
    -----------
    spaceranger_output_dir : str
        Path to the SpaceRanger 'outs' directory
    dataset_id : str
        Optional identifier for the dataset

    Returns:
    --------
    sdata : SpatialData
        SpatialData object containing all VisiumHD data layers
    """
    print(f"\n{'='*80}")
    print("LOADING VISIUMHD DATA")
    print(f"{'='*80}")

    print(f"Loading data from: {spaceranger_output_dir}")

    # Load VisiumHD data (includes images, shapes, and tables at multiple resolutions)
    sdata = sio.visium_hd(spaceranger_output_dir, dataset_id=dataset_id)

    print(f"✓ Data loaded successfully")
    print(f"  Available tables: {list(sdata.tables.keys())}")
    print(f"  Available images: {list(sdata.images.keys())}")
    print(f"  Available shapes: {list(sdata.shapes.keys())}")

    return sdata


def cache_to_zarr(sdata: sd.SpatialData, zarr_path: str, reload: bool = True):
    """
    Cache SpatialData to ZARR format for faster subsequent loading.

    Best Practice:
    - ZARR format enables lazy loading and faster I/O
    - Essential for large VisiumHD datasets (>1GB)
    - Allows memory-efficient operations

    Parameters:
    -----------
    sdata : SpatialData
        SpatialData object to cache
    zarr_path : str
        Path where ZARR store will be saved
    reload : bool
        If True, reload from ZARR and return the reloaded object

    Returns:
    --------
    sdata : SpatialData or None
        Reloaded SpatialData if reload=True, else None
    """
    print(f"\nCaching to ZARR: {zarr_path}")
    sdata.write(zarr_path, overwrite=True)

    if reload:
        # Clear memory before reloading
        del sdata
        gc.collect()

        print(f"Reloading from ZARR...")
        sdata = sd.read_zarr(zarr_path)
        print(f"✓ Reloaded from ZARR")
        return sdata

    return None


# ============================================================================
# SECTION 2: SPATIAL DATA PREPROCESSING
# ============================================================================

def crop_to_tissue_region(sdata: sd.SpatialData,
                          x_min: float, x_max: float,
                          y_min: float, y_max: float,
                          coordinate_system: str = "") -> sd.SpatialData:
    """
    Crop SpatialData to a specific tissue region.

    Best Practice:
    - Reduces memory usage by focusing on region of interest
    - Important for VisiumHD which can have millions of bins
    - Use coordinate_system="" for default coordinate system

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    x_min, x_max, y_min, y_max : float
        Bounding box coordinates in microns
    coordinate_system : str
        Name of the coordinate system (default: "")

    Returns:
    --------
    sdata : SpatialData
        Cropped SpatialData object
    """
    print(f"\n{'='*80}")
    print("CROPPING TO TISSUE REGION")
    print(f"{'='*80}")

    print(f"Bounding box: x=[{x_min}, {x_max}], y=[{y_min}, {y_max}]")

    sdata = sdata.query.bounding_box(
        axes=("x", "y"),
        min_coordinate=np.array([x_min, y_min]),
        max_coordinate=np.array([x_max, y_max]),
        target_coordinate_system=coordinate_system,
        filter_table=False  # Keep all cells, just update coordinates
    )

    print(f"✓ Cropped successfully")
    return sdata


def annotate_spatial_regions(sdata: sd.SpatialData,
                             polygons: dict,
                             annotation_key: str = 'region',
                             resolutions: list = None) -> sd.SpatialData:
    """
    Annotate spatial regions using polygons (e.g., cell types, tissue types).

    Best Practice:
    - Define regions using Shapely Polygon objects
    - Annotate all resolutions consistently
    - Use meaningful annotation keys

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    polygons : dict
        Dictionary mapping region names to Shapely Polygon objects
        Example: {'tumor': Polygon([...]), 'normal': Polygon([...])}
    annotation_key : str
        Column name for storing annotations in obs
    resolutions : list
        List of resolutions to annotate (e.g., ['002um', '008um', '016um'])
        If None, annotates all available square tables

    Returns:
    --------
    sdata : SpatialData
        SpatialData with annotated regions
    """
    print(f"\n{'='*80}")
    print("ANNOTATING SPATIAL REGIONS")
    print(f"{'='*80}")

    if resolutions is None:
        # Find all square tables
        resolutions = [k.split('_')[-1] for k in sdata.tables.keys() if k.startswith('square_')]

    print(f"Regions to annotate: {list(polygons.keys())}")
    print(f"Resolutions: {resolutions}")

    for resolution in resolutions:
        table_name = f'square_{resolution}'
        if table_name not in sdata.tables:
            print(f"  ⚠ Skipping {table_name} (not found)")
            continue

        # Initialize annotation column
        sdata.tables[table_name].obs[annotation_key] = 'N/A'

        # Annotate each region
        for region_name, polygon in polygons.items():
            print(f"  Processing {region_name} at {resolution}...")

            # Query bins within polygon
            filtered = polygon_query(
                sdata,
                polygon=polygon,
                target_coordinate_system="",
            )

            # Update annotations
            matching_bins = filtered.tables[table_name].obs_names
            sdata.tables[table_name].obs.loc[matching_bins, annotation_key] = region_name

            n_bins = len(matching_bins)
            print(f"    ✓ Annotated {n_bins:,} bins as '{region_name}'")

    print(f"✓ Annotation complete")
    return sdata


# ============================================================================
# SECTION 3: QUALITY CONTROL AND VISUALIZATION
# ============================================================================

def plot_tissue_overview(sdata: sd.SpatialData,
                        image_key: str = "_hires_image",
                        save_path: str = None):
    """
    Plot tissue overview with H&E staining.

    Best Practice:
    - Always start analysis with tissue visualization
    - Use hires_image for publication-quality figures
    - Verify tissue integrity and region selection
    """
    print(f"\n{'='*80}")
    print("PLOTTING TISSUE OVERVIEW")
    print(f"{'='*80}")

    fig = (sdata.pl.render_images(image_key)
           .pl.show(coordinate_systems="", figsize=(12, 12),
                   na_in_legend=False, title="H&E Stain Overview",
                   return_ax=False))

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {save_path}")

    plt.show()


def compute_qc_metrics(sdata: sd.SpatialData,
                      resolution: str = '016um',
                      mt_pattern: str = '^MT-') -> sd.SpatialData:
    """
    Compute quality control metrics for spatial data.

    Best Practice:
    - Compute QC metrics at your analysis resolution
    - Check for mitochondrial content (tissue quality)
    - Identify low-quality bins early

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    resolution : str
        Resolution to analyze (e.g., '002um', '008um', '016um')
    mt_pattern : str
        Regex pattern for mitochondrial genes

    Returns:
    --------
    sdata : SpatialData
        SpatialData with QC metrics added to table.obs
    """
    print(f"\n{'='*80}")
    print(f"COMPUTING QC METRICS (resolution: {resolution})")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    # Compute standard QC metrics
    sc.pp.calculate_qc_metrics(
        table,
        qc_vars=['mt'],
        percent_top=None,
        log1p=False,
        inplace=True
    )

    # Add mitochondrial gene percentage
    table.var['mt'] = table.var_names.str.match(mt_pattern)
    table.obs['pct_counts_mt'] = (
        table[:, table.var['mt']].X.sum(1).A1 /
        table.obs['total_counts']
    ) * 100

    # Summary statistics
    print(f"\n{'='*80}")
    print("QC METRICS SUMMARY")
    print(f"{'='*80}")
    print(f"Total bins: {table.n_obs:,}")
    print(f"Total genes: {table.n_vars:,}")
    print(f"Median UMIs per bin: {np.median(table.obs['total_counts']):.0f}")
    print(f"Median genes per bin: {np.median(table.obs['n_genes_by_counts']):.0f}")
    print(f"Median MT%: {np.median(table.obs['pct_counts_mt']):.2f}%")

    return sdata


def plot_qc_spatial(sdata: sd.SpatialData,
                   resolution: str = '016um',
                   metrics: list = ['total_counts', 'n_genes_by_counts', 'pct_counts_mt'],
                   save_prefix: str = None):
    """
    Plot QC metrics on spatial coordinates.

    Best Practice:
    - Visualize QC metrics spatially to identify artifacts
    - Look for edge effects, processing artifacts, or tissue damage
    - Use consistent color scales across samples
    """
    print(f"\n{'='*80}")
    print("PLOTTING SPATIAL QC METRICS")
    print(f"{'='*80}")

    n_metrics = len(metrics)
    fig, axes = plt.subplots(1, n_metrics, figsize=(6*n_metrics, 6))

    if n_metrics == 1:
        axes = [axes]

    for i, metric in enumerate(metrics):
        print(f"  Plotting {metric}...")

        # Render on tissue
        (sdata.pl.render_images("_hires_image", alpha=0.5)
         .pl.render_shapes(element=f'_square_{resolution}', color=metric, method='matplotlib')
         .pl.show(coordinate_systems="", ax=axes[i],
                 title=metric, na_in_legend=False))

    plt.tight_layout()

    if save_prefix:
        save_path = f"{save_prefix}_qc_spatial.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {save_path}")

    plt.show()


# ============================================================================
# SECTION 4: SPATIAL ANALYSIS WITH SQUIDPY
# ============================================================================

def compute_spatial_features(sdata: sd.SpatialData,
                            resolution: str = '016um') -> sd.SpatialData:
    """
    Compute spatial features using squidpy.

    Best Practice:
    - Extract spatial coordinates from bin names
    - Compute spatial neighbors for downstream analysis
    - Calculate spatial autocorrelation for key genes

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    resolution : str
        Resolution for analysis

    Returns:
    --------
    sdata : SpatialData
        SpatialData with spatial features computed
    """
    print(f"\n{'='*80}")
    print(f"COMPUTING SPATIAL FEATURES WITH SQUIDPY")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    # Extract spatial coordinates from bin names
    # VisiumHD bin names format: square_002um_00123_04567-1
    print("Extracting spatial coordinates...")
    coords = []
    for bin_name in table.obs_names:
        parts = bin_name.split('_')
        if len(parts) >= 4:
            y_coord = int(parts[2])
            x_coord = int(parts[3].split('-')[0])
            coords.append([x_coord, y_coord])
        else:
            coords.append([np.nan, np.nan])

    table.obsm['spatial'] = np.array(coords)

    # Compute spatial neighbors
    print("Computing spatial neighbors...")
    sq.gr.spatial_neighbors(table, coord_type='generic', delaunay=False)

    print(f"✓ Spatial features computed")
    print(f"  Spatial neighbors graph: {table.obsp['spatial_connectivities'].shape}")

    return sdata


def compute_spatial_autocorrelation(sdata: sd.SpatialData,
                                   resolution: str = '016um',
                                   genes: list = None,
                                   mode: str = 'moran') -> pd.DataFrame:
    """
    Compute spatial autocorrelation (Moran's I or Geary's C).

    Best Practice:
    - Use Moran's I to identify spatially variable genes
    - Focus analysis on highly variable or marker genes
    - Essential for understanding spatial expression patterns

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    resolution : str
        Resolution for analysis
    genes : list
        List of genes to analyze (None = all genes)
    mode : str
        'moran' for Moran's I or 'geary' for Geary's C

    Returns:
    --------
    results : pd.DataFrame
        Spatial autocorrelation results
    """
    print(f"\n{'='*80}")
    print(f"COMPUTING SPATIAL AUTOCORRELATION ({mode.upper()})")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    # Ensure spatial neighbors are computed
    if 'spatial_connectivities' not in table.obsp:
        print("  Computing spatial neighbors first...")
        sq.gr.spatial_neighbors(table, coord_type='generic', delaunay=False)

    # Compute autocorrelation
    print(f"  Analyzing {len(genes) if genes else table.n_vars} genes...")
    sq.gr.spatial_autocorr(
        table,
        mode=mode,
        genes=genes,
        n_jobs=-1  # Use all CPUs
    )

    results = table.uns[f'{mode}_I' if mode == 'moran' else f'{mode}_C']
    print(f"✓ Autocorrelation computed")

    # Show top spatially variable genes
    print(f"\nTop 10 spatially variable genes:")
    if mode == 'moran':
        top_genes = results.sort_values('I', ascending=False).head(10)
        print(top_genes[['I', 'pval_norm']])
    else:
        top_genes = results.sort_values('C').head(10)
        print(top_genes[['C', 'pval_norm']])

    return results


def spatial_clustering(sdata: sd.SpatialData,
                       resolution: str = '016um',
                       n_clusters: int = 10) -> sd.SpatialData:
    """
    Perform spatial clustering using GIFTwrap's spatial recipe.

    Best Practice:
    - Combines expression and spatial information
    - Use appropriate number of clusters for your tissue
    - Validate clusters with known markers

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    resolution : str
        Resolution for clustering
    n_clusters : int
        Number of spatial clusters

    Returns:
    --------
    sdata : SpatialData
        SpatialData with clusters in table.obs
    """
    print(f"\n{'='*80}")
    print(f"SPATIAL CLUSTERING (n_clusters={n_clusters})")
    print(f"{'='*80}")

    # Use GIFTwrap's spatial clustering recipe
    print("Running spatial expression co-clustering...")
    sdata = gw.sp.recipe_spatial_expression_coclustering(
        sdata,
        table_name=f'square_{resolution}',
        n_highly_variable_genes=2000,
        coordinate_system=""
    )

    print(f"✓ Clustering complete")
    print(f"  Cluster key: 'spatio_expression_coclustering'")

    return sdata


def plot_spatial_clusters(sdata: sd.SpatialData,
                         resolution: str = '016um',
                         cluster_key: str = 'spatio_expression_coclustering',
                         save_path: str = None):
    """
    Visualize spatial clusters on tissue.

    Best Practice:
    - Overlay clusters on H&E image
    - Use distinct colors for clusters
    - Verify biological relevance
    """
    print(f"\n{'='*80}")
    print("PLOTTING SPATIAL CLUSTERS")
    print(f"{'='*80}")

    fig = (sdata.pl.render_images("_hires_image", alpha=0.5)
           .pl.render_shapes(element=f'_square_{resolution}',
                           color=cluster_key,
                           method='matplotlib',
                           palette='tab20')
           .pl.show(coordinate_systems="", figsize=(12, 12),
                   title="Spatial Clusters", na_in_legend=False))

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {save_path}")

    plt.show()


# ============================================================================
# SECTION 5: CELL TYPE ANNOTATION
# ============================================================================

def annotate_celltypes_by_markers(sdata: sd.SpatialData,
                                  marker_genes: dict,
                                  resolution: str = '016um',
                                  method: str = 'threshold') -> sd.SpatialData:
    """
    Annotate cell types using marker gene expression.

    Best Practice:
    - Use well-established marker genes from literature
    - Validate with multiple markers per cell type
    - Consider tissue-specific markers

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    marker_genes : dict
        Dictionary mapping cell type names to lists of marker genes
        Example: {'T_cell': ['CD3D', 'CD3E'], 'B_cell': ['CD19', 'MS4A1']}
    resolution : str
        Resolution for annotation
    method : str
        'threshold' (>0 expression) or 'score' (aggregate score)

    Returns:
    --------
    sdata : SpatialData
        SpatialData with cell type annotations in table.obs['celltype']
    """
    print(f"\n{'='*80}")
    print("ANNOTATING CELL TYPES BY MARKER GENES")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    print(f"Cell types to annotate: {list(marker_genes.keys())}")

    # Initialize cell type column
    table.obs['celltype'] = 'Unknown'
    table.obs['celltype_score'] = 0.0

    # Normalize data if not already done
    if 'log1p' not in table.uns:
        print("  Normalizing and log-transforming data...")
        sc.pp.normalize_total(table, target_sum=1e4)
        sc.pp.log1p(table)

    # Score each cell type
    for celltype, markers in marker_genes.items():
        # Filter markers present in data
        available_markers = [g for g in markers if g in table.var_names]

        if len(available_markers) == 0:
            print(f"  ⚠ No markers found for {celltype}")
            continue

        print(f"  Scoring {celltype} ({len(available_markers)}/{len(markers)} markers available)...")

        # Compute marker score
        sc.tl.score_genes(table, available_markers, score_name=f'{celltype}_score')

        # Assign cell type based on highest score
        if method == 'threshold':
            # Threshold: at least one marker expressed
            marker_expr = table[:, available_markers].X.toarray() if hasattr(table.X, 'toarray') else table[:, available_markers].X
            has_marker = (marker_expr > 0).any(axis=1)
            mask = has_marker
        else:  # method == 'score'
            # Score-based: highest aggregate score
            score = table.obs[f'{celltype}_score']
            mask = score > table.obs['celltype_score']

        # Update annotations
        table.obs.loc[mask, 'celltype'] = celltype
        table.obs.loc[mask, 'celltype_score'] = table.obs.loc[mask, f'{celltype}_score']

    # Report results
    celltype_counts = table.obs['celltype'].value_counts()
    print(f"\n✓ Cell type annotation complete")
    print(f"\nCell type distribution:")
    print(celltype_counts)

    return sdata


def annotate_celltypes_from_reference(sdata: sd.SpatialData,
                                      reference_adata: ad.AnnData,
                                      celltype_key: str = 'celltype',
                                      resolution: str = '016um',
                                      n_genes: int = 3000) -> sd.SpatialData:
    """
    Annotate cell types using a single-cell reference dataset.

    Best Practice:
    - Use high-quality scRNA-seq reference from same tissue
    - Filter to highly variable genes shared between datasets
    - Use ingest for label transfer

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData object
    reference_adata : AnnData
        scRNA-seq reference with cell type labels
    celltype_key : str
        Column in reference_adata.obs with cell type labels
    resolution : str
        Resolution for annotation
    n_genes : int
        Number of highly variable genes for integration

    Returns:
    --------
    sdata : SpatialData
        SpatialData with transferred cell type labels
    """
    print(f"\n{'='*80}")
    print("ANNOTATING CELL TYPES FROM REFERENCE DATASET")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    print(f"Reference dataset: {reference_adata.n_obs} cells, {reference_adata.n_vars} genes")
    print(f"Spatial dataset: {table.n_obs} bins, {table.n_vars} genes")

    # Preprocessing
    print("\n  Preprocessing reference...")
    sc.pp.normalize_total(reference_adata, target_sum=1e4)
    sc.pp.log1p(reference_adata)
    sc.pp.highly_variable_genes(reference_adata, n_top_genes=n_genes)

    print("  Preprocessing spatial...")
    sc.pp.normalize_total(table, target_sum=1e4)
    sc.pp.log1p(table)

    # Find shared highly variable genes
    ref_hvg = reference_adata.var_names[reference_adata.var['highly_variable']].tolist()
    shared_genes = list(set(ref_hvg) & set(table.var_names))
    print(f"\n  Shared HVGs: {len(shared_genes)}")

    if len(shared_genes) < 100:
        print("  ⚠ Warning: Few shared genes may reduce annotation quality")

    # Subset to shared genes
    ref_subset = reference_adata[:, shared_genes].copy()
    spatial_subset = table[:, shared_genes].copy()

    # PCA on reference
    print("  Computing PCA on reference...")
    sc.tl.pca(ref_subset, n_comps=30)

    # Use ingest for label transfer
    print("  Transferring cell type labels...")
    sc.tl.ingest(spatial_subset, ref_subset, obs=celltype_key)

    # Transfer labels back to main table
    table.obs[f'{celltype_key}_transferred'] = spatial_subset.obs[celltype_key]

    # Report results
    celltype_counts = table.obs[f'{celltype_key}_transferred'].value_counts()
    print(f"\n✓ Cell type transfer complete")
    print(f"\nTransferred cell type distribution:")
    print(celltype_counts)

    return sdata


def compute_celltype_proportions(sdata: sd.SpatialData,
                                 resolution: str = '016um',
                                 celltype_key: str = 'celltype',
                                 region_key: str = None) -> pd.DataFrame:
    """
    Compute cell type proportions overall or by region.

    Best Practice:
    - Quantify cell type composition
    - Compare across spatial regions
    - Useful for tissue organization analysis

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData with cell type annotations
    resolution : str
        Resolution for analysis
    celltype_key : str
        Column with cell type annotations
    region_key : str
        Optional column with region annotations (e.g., 'tissue_region')

    Returns:
    --------
    proportions : pd.DataFrame
        Cell type proportions (by region if region_key provided)
    """
    print(f"\n{'='*80}")
    print("COMPUTING CELL TYPE PROPORTIONS")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    if region_key is None:
        # Overall proportions
        counts = table.obs[celltype_key].value_counts()
        proportions = (counts / counts.sum() * 100).to_frame('percentage')
        proportions['count'] = counts

        print("\nOverall cell type proportions:")
        print(proportions)

    else:
        # Proportions by region
        proportions = (
            table.obs.groupby([region_key, celltype_key])
            .size()
            .reset_index(name='count')
        )

        # Calculate percentages within each region
        proportions['percentage'] = proportions.groupby(region_key)['count'].transform(
            lambda x: 100 * x / x.sum()
        )

        print(f"\nCell type proportions by {region_key}:")
        print(proportions.pivot(index=celltype_key, columns=region_key, values='percentage'))

    return proportions


def plot_celltypes_spatial(sdata: sd.SpatialData,
                           resolution: str = '016um',
                           celltype_key: str = 'celltype',
                           save_path: str = None):
    """
    Visualize cell types on spatial coordinates.

    Best Practice:
    - Overlay on tissue image
    - Use distinct colors for cell types
    - Verify spatial organization matches biology
    """
    print(f"\n{'='*80}")
    print("PLOTTING CELL TYPES ON TISSUE")
    print(f"{'='*80}")

    fig = (sdata.pl.render_images("_hires_image", alpha=0.5)
           .pl.render_shapes(element=f'_square_{resolution}',
                           color=celltype_key,
                           method='matplotlib',
                           palette='tab20')
           .pl.show(coordinate_systems="", figsize=(12, 12),
                   title="Cell Type Annotations", na_in_legend=False))

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {save_path}")

    plt.show()


def plot_marker_genes_spatial(sdata: sd.SpatialData,
                              genes: list,
                              resolution: str = '016um',
                              ncols: int = 3,
                              save_path: str = None):
    """
    Plot marker gene expression on spatial coordinates.

    Best Practice:
    - Visualize key markers to validate cell type assignments
    - Compare expression patterns with annotations
    - Use consistent color scales
    """
    print(f"\n{'='*80}")
    print(f"PLOTTING MARKER GENES: {', '.join(genes)}")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    # Filter to available genes
    available_genes = [g for g in genes if g in table.var_names]

    if len(available_genes) == 0:
        print("  ⚠ None of the specified genes found in data")
        return

    print(f"  Plotting {len(available_genes)}/{len(genes)} genes")

    nrows = int(np.ceil(len(available_genes) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(6*ncols, 6*nrows))

    if nrows == 1 and ncols == 1:
        axes = [[axes]]
    elif nrows == 1:
        axes = [axes]

    for idx, gene in enumerate(available_genes):
        row = idx // ncols
        col = idx % ncols

        # Get expression values
        gene_expr = table[:, gene].X.toarray().flatten() if hasattr(table.X, 'toarray') else table[:, gene].X.flatten()

        # Add to obs temporarily
        table.obs[f'_tmp_{gene}'] = gene_expr

        # Plot
        ax = axes[row][col] if nrows > 1 else axes[col]
        (sdata.pl.render_images("_hires_image", alpha=0.3)
         .pl.render_shapes(element=f'_square_{resolution}',
                         color=f'_tmp_{gene}',
                         method='matplotlib',
                         cmap='viridis')
         .pl.show(coordinate_systems="", ax=ax,
                 title=gene, na_in_legend=False))

        # Clean up
        table.obs.drop(columns=f'_tmp_{gene}', inplace=True)

    # Remove empty subplots
    for idx in range(len(available_genes), nrows * ncols):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row][col] if nrows > 1 else axes[col]
        ax.axis('off')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {save_path}")

    plt.show()


# ============================================================================
# SECTION 6: MULTI-SAMPLE INTEGRATION AND ANALYSIS
# ============================================================================

def load_multiple_samples(sample_dirs: dict,
                         cache_dir: str = "./cache") -> dict:
    """
    Load multiple VisiumHD samples for joint analysis.

    Best Practice:
    - Load each sample separately first
    - Cache to ZARR for memory efficiency
    - Use consistent naming scheme

    Parameters:
    -----------
    sample_dirs : dict
        Dictionary mapping sample names to SpaceRanger output directories
        Example: {'sample1': '/path/to/sample1/outs', 'sample2': '/path/to/sample2/outs'}
    cache_dir : str
        Directory for ZARR cache files

    Returns:
    --------
    samples : dict
        Dictionary mapping sample names to SpatialData objects
    """
    print(f"\n{'='*80}")
    print("LOADING MULTIPLE SAMPLES")
    print(f"{'='*80}")

    os.makedirs(cache_dir, exist_ok=True)
    samples = {}

    for sample_name, sample_dir in sample_dirs.items():
        print(f"\nProcessing {sample_name}...")

        # Load sample
        sdata = load_visiumhd_data(sample_dir, dataset_id=sample_name)

        # Cache to ZARR
        zarr_path = os.path.join(cache_dir, f"{sample_name}.zarr")
        sdata = cache_to_zarr(sdata, zarr_path, reload=True)

        samples[sample_name] = sdata

    print(f"\n✓ Loaded {len(samples)} samples")
    return samples


def concatenate_spatial_tables(samples: dict,
                               resolution: str = '016um',
                               add_sample_key: bool = True,
                               sample_key: str = 'sample') -> ad.AnnData:
    """
    Concatenate expression tables from multiple spatial samples.

    Best Practice:
    - Concatenate for joint analysis (UMAP, clustering, DE)
    - Add sample labels to track origin
    - Use for cross-sample comparisons

    Parameters:
    -----------
    samples : dict
        Dictionary of sample_name -> SpatialData objects
    resolution : str
        Resolution to extract
    add_sample_key : bool
        If True, add sample labels to obs
    sample_key : str
        Column name for sample labels

    Returns:
    --------
    combined_adata : AnnData
        Concatenated expression matrix with all samples
    """
    print(f"\n{'='*80}")
    print(f"CONCATENATING TABLES FROM {len(samples)} SAMPLES")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    adatas = []

    for sample_name, sdata in samples.items():
        if table_name not in sdata.tables:
            print(f"  ⚠ Skipping {sample_name}: {table_name} not found")
            continue

        adata = sdata.tables[table_name].copy()

        if add_sample_key:
            adata.obs[sample_key] = sample_name

        # Preserve spatial coordinates
        if 'spatial' not in adata.obsm:
            coords = []
            for bin_name in adata.obs_names:
                parts = bin_name.split('_')
                if len(parts) >= 4:
                    y_coord = int(parts[2])
                    x_coord = int(parts[3].split('-')[0])
                    coords.append([x_coord, y_coord])
                else:
                    coords.append([np.nan, np.nan])
            adata.obsm['spatial'] = np.array(coords)

        adatas.append(adata)
        print(f"  Added {sample_name}: {adata.n_obs:,} bins, {adata.n_vars:,} genes")

    if len(adatas) == 0:
        raise ValueError("No valid samples found")

    # Concatenate
    print("\n  Concatenating...")
    combined_adata = ad.concat(adatas, label=sample_key if not add_sample_key else None,
                               join='inner')  # Only keep shared genes

    print(f"\n✓ Concatenation complete")
    print(f"  Total bins: {combined_adata.n_obs:,}")
    print(f"  Shared genes: {combined_adata.n_vars:,}")
    print(f"  Samples: {combined_adata.obs[sample_key].unique().tolist()}")

    return combined_adata


def integrate_samples_batch_correction(combined_adata: ad.AnnData,
                                       batch_key: str = 'sample',
                                       n_hvgs: int = 3000) -> ad.AnnData:
    """
    Integrate multiple samples with batch correction.

    Best Practice:
    - Use when samples show strong batch effects
    - Harmony or scVI recommended for VisiumHD
    - Preserve biological variation while removing technical effects

    Parameters:
    -----------
    combined_adata : AnnData
        Concatenated expression matrix
    batch_key : str
        Column in obs with batch/sample labels
    n_hvgs : int
        Number of highly variable genes

    Returns:
    --------
    combined_adata : AnnData
        Batch-corrected data in .obsm['X_pca']
    """
    print(f"\n{'='*80}")
    print("BATCH CORRECTION AND INTEGRATION")
    print(f"{'='*80}")

    print(f"  Batches: {combined_adata.obs[batch_key].value_counts().to_dict()}")

    # Preprocessing
    print("\n  Preprocessing...")
    sc.pp.normalize_total(combined_adata, target_sum=1e4)
    sc.pp.log1p(combined_adata)
    sc.pp.highly_variable_genes(combined_adata, n_top_genes=n_hvgs, batch_key=batch_key)

    # PCA on HVGs
    print("  Computing PCA...")
    sc.tl.pca(combined_adata, n_comps=50, use_highly_variable=True)

    # Batch correction with Harmony
    print("  Running Harmony batch correction...")
    try:
        import scanpy.external as sce
        sce.pp.harmony_integrate(combined_adata, key=batch_key, basis='X_pca', adjusted_basis='X_pca_harmony')
        print("  ✓ Using Harmony-corrected PCA for downstream analysis")
        use_rep = 'X_pca_harmony'
    except ImportError:
        print("  ⚠ Harmony not available, using uncorrected PCA")
        print("    Install with: pip install harmonypy")
        use_rep = 'X_pca'

    # UMAP
    print("  Computing UMAP...")
    sc.pp.neighbors(combined_adata, n_neighbors=30, use_rep=use_rep)
    sc.tl.umap(combined_adata)

    # Clustering
    print("  Clustering...")
    sc.tl.leiden(combined_adata, resolution=1.0)

    print(f"\n✓ Integration complete")
    return combined_adata


def compare_samples_composition(combined_adata: ad.AnnData,
                                sample_key: str = 'sample',
                                cluster_key: str = 'leiden',
                                celltype_key: str = None) -> pd.DataFrame:
    """
    Compare cluster or cell type composition across samples.

    Best Practice:
    - Quantify differences between tissue sections
    - Identify sample-specific populations
    - Statistical testing for significant differences

    Parameters:
    -----------
    combined_adata : AnnData
        Integrated data with sample labels
    sample_key : str
        Column with sample labels
    cluster_key : str
        Column with cluster assignments
    celltype_key : str
        Optional column with cell type annotations

    Returns:
    --------
    composition_df : pd.DataFrame
        Composition matrix (clusters/celltypes × samples)
    """
    print(f"\n{'='*80}")
    print("COMPARING SAMPLE COMPOSITION")
    print(f"{'='*80}")

    # Use celltype if available, otherwise clusters
    group_key = celltype_key if celltype_key and celltype_key in combined_adata.obs else cluster_key

    # Compute proportions
    composition = (
        combined_adata.obs.groupby([sample_key, group_key])
        .size()
        .reset_index(name='count')
    )

    # Calculate percentages within each sample
    composition['percentage'] = composition.groupby(sample_key)['count'].transform(
        lambda x: 100 * x / x.sum()
    )

    # Pivot to matrix format
    composition_matrix = composition.pivot(index=group_key, columns=sample_key, values='percentage')
    composition_matrix = composition_matrix.fillna(0)

    print(f"\nComposition matrix ({group_key} × {sample_key}):")
    print(composition_matrix)

    # Plot stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    composition_matrix.T.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
    ax.set_ylabel('Percentage')
    ax.set_xlabel('Sample')
    ax.set_title(f'{group_key.capitalize()} Composition Across Samples')
    ax.legend(title=group_key, bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return composition_matrix


def plot_integrated_umap(combined_adata: ad.AnnData,
                        sample_key: str = 'sample',
                        color_by: list = None,
                        ncols: int = 2,
                        save_path: str = None):
    """
    Plot UMAP colored by sample, clusters, and cell types.

    Best Practice:
    - Verify good mixing between samples
    - Check for batch effects
    - Visualize biological vs technical variation

    Parameters:
    -----------
    combined_adata : AnnData
        Integrated data with UMAP
    sample_key : str
        Column with sample labels
    color_by : list
        List of columns to color UMAP by
    ncols : int
        Number of columns for subplots
    save_path : str
        Optional path to save figure
    """
    print(f"\n{'='*80}")
    print("PLOTTING INTEGRATED UMAP")
    print(f"{'='*80}")

    if color_by is None:
        color_by = [sample_key]
        if 'leiden' in combined_adata.obs:
            color_by.append('leiden')
        if 'celltype' in combined_adata.obs:
            color_by.append('celltype')

    nrows = int(np.ceil(len(color_by) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(6*ncols, 5*nrows))

    if nrows == 1 and ncols == 1:
        axes = [[axes]]
    elif nrows == 1:
        axes = [axes]

    for idx, color_key in enumerate(color_by):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row][col] if nrows > 1 else axes[col]

        sc.pl.umap(combined_adata, color=color_key, ax=ax, show=False,
                  title=f'UMAP colored by {color_key}')

    # Remove empty subplots
    for idx in range(len(color_by), nrows * ncols):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row][col] if nrows > 1 else axes[col]
        ax.axis('off')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {save_path}")

    plt.show()


def transfer_annotations_between_samples(samples: dict,
                                         reference_sample: str,
                                         target_sample: str,
                                         annotation_key: str,
                                         resolution: str = '016um',
                                         n_neighbors: int = 30) -> dict:
    """
    Transfer annotations from one sample to another using kNN.

    Best Practice:
    - Transfer cell type labels from annotated to new sample
    - Useful for serial sections or adjacent tissue regions
    - Validate transferred labels with markers

    Parameters:
    -----------
    samples : dict
        Dictionary of sample_name -> SpatialData objects
    reference_sample : str
        Name of sample with annotations
    target_sample : str
        Name of sample to transfer annotations to
    annotation_key : str
        Column in reference with annotations to transfer
    resolution : str
        Resolution for analysis
    n_neighbors : int
        Number of neighbors for label transfer

    Returns:
    --------
    samples : dict
        Updated samples dictionary with transferred annotations
    """
    print(f"\n{'='*80}")
    print(f"TRANSFERRING ANNOTATIONS: {reference_sample} → {target_sample}")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'

    # Get tables
    ref_table = samples[reference_sample].tables[table_name]
    target_table = samples[target_sample].tables[table_name]

    print(f"  Reference: {ref_table.n_obs:,} bins with '{annotation_key}'")
    print(f"  Target: {target_table.n_obs:,} bins")

    if annotation_key not in ref_table.obs:
        raise ValueError(f"Annotation key '{annotation_key}' not found in reference")

    # Find shared genes
    shared_genes = list(set(ref_table.var_names) & set(target_table.var_names))
    print(f"  Shared genes: {len(shared_genes)}")

    if len(shared_genes) < 100:
        print("  ⚠ Warning: Few shared genes may reduce transfer quality")

    # Subset to shared genes
    ref_subset = ref_table[:, shared_genes].copy()
    target_subset = target_table[:, shared_genes].copy()

    # Normalize
    print("\n  Preprocessing...")
    sc.pp.normalize_total(ref_subset, target_sum=1e4)
    sc.pp.log1p(ref_subset)
    sc.pp.normalize_total(target_subset, target_sum=1e4)
    sc.pp.log1p(target_subset)

    # PCA on reference
    print("  Computing PCA on reference...")
    sc.pp.highly_variable_genes(ref_subset, n_top_genes=2000)
    sc.tl.pca(ref_subset, n_comps=30, use_highly_variable=True)

    # Transfer labels using ingest
    print("  Transferring labels...")
    sc.tl.ingest(target_subset, ref_subset, obs=annotation_key)

    # Add transferred labels to main table
    samples[target_sample].tables[table_name].obs[f'{annotation_key}_transferred'] = \
        target_subset.obs[annotation_key]

    # Report
    transfer_counts = target_subset.obs[annotation_key].value_counts()
    print(f"\n✓ Transfer complete")
    print(f"\nTransferred labels:")
    print(transfer_counts)

    return samples


def compare_spatial_patterns(samples: dict,
                             gene: str,
                             resolution: str = '016um',
                             figsize: tuple = (12, 6)):
    """
    Compare spatial expression patterns of a gene across samples.

    Best Practice:
    - Identify conserved spatial patterns
    - Detect sample-specific expression
    - Use same color scale for fair comparison

    Parameters:
    -----------
    samples : dict
        Dictionary of sample_name -> SpatialData objects
    gene : str
        Gene name to compare
    resolution : str
        Resolution for plotting
    figsize : tuple
        Figure size
    """
    print(f"\n{'='*80}")
    print(f"COMPARING SPATIAL PATTERN: {gene}")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    n_samples = len(samples)

    fig, axes = plt.subplots(1, n_samples, figsize=figsize)
    if n_samples == 1:
        axes = [axes]

    # Find global min/max for consistent color scale
    vmin, vmax = np.inf, -np.inf
    for sample_name, sdata in samples.items():
        table = sdata.tables[table_name]
        if gene in table.var_names:
            expr = table[:, gene].X.toarray().flatten() if hasattr(table.X, 'toarray') else table[:, gene].X.flatten()
            vmin = min(vmin, expr.min())
            vmax = max(vmax, expr.max())

    # Plot each sample
    for idx, (sample_name, sdata) in enumerate(samples.items()):
        table = sdata.tables[table_name]

        if gene not in table.var_names:
            axes[idx].text(0.5, 0.5, f'{gene} not found\nin {sample_name}',
                          ha='center', va='center', transform=axes[idx].transAxes)
            axes[idx].axis('off')
            continue

        # Get expression
        expr = table[:, gene].X.toarray().flatten() if hasattr(table.X, 'toarray') else table[:, gene].X.flatten()
        table.obs[f'_tmp_{gene}'] = expr

        # Plot
        (sdata.pl.render_images("_hires_image", alpha=0.3)
         .pl.render_shapes(element=f'_square_{resolution}',
                         color=f'_tmp_{gene}',
                         method='matplotlib',
                         cmap='viridis',
                         vmin=vmin,
                         vmax=vmax)
         .pl.show(coordinate_systems="", ax=axes[idx],
                 title=f'{sample_name}\n{gene}', na_in_legend=False))

        # Clean up
        table.obs.drop(columns=f'_tmp_{gene}', inplace=True)

    plt.tight_layout()
    plt.show()


def differential_expression_between_samples(combined_adata: ad.AnnData,
                                           sample_key: str = 'sample',
                                           sample1: str = None,
                                           sample2: str = None,
                                           n_genes: int = 50) -> pd.DataFrame:
    """
    Find differentially expressed genes between samples.

    Best Practice:
    - Identify sample-specific markers
    - Compare tissue regions or conditions
    - Use Wilcoxon rank-sum test for robustness

    Parameters:
    -----------
    combined_adata : AnnData
        Integrated data with sample labels
    sample_key : str
        Column with sample labels
    sample1, sample2 : str
        Sample names to compare (if None, compares all pairs)
    n_genes : int
        Number of top genes to return

    Returns:
    --------
    de_results : pd.DataFrame
        Differential expression results
    """
    print(f"\n{'='*80}")
    print("DIFFERENTIAL EXPRESSION BETWEEN SAMPLES")
    print(f"{'='*80}")

    if sample1 and sample2:
        print(f"  Comparing: {sample1} vs {sample2}")

        # Subset to samples
        mask = combined_adata.obs[sample_key].isin([sample1, sample2])
        adata_subset = combined_adata[mask].copy()

        # Run DE test
        sc.tl.rank_genes_groups(adata_subset, groupby=sample_key,
                               groups=[sample1], reference=sample2,
                               method='wilcoxon')

        # Extract results
        de_results = sc.get.rank_genes_groups_df(adata_subset, group=sample1)

    else:
        print(f"  Comparing all samples pairwise")

        # Run DE test for all groups
        sc.tl.rank_genes_groups(combined_adata, groupby=sample_key,
                               method='wilcoxon')

        # Extract results for first group
        groups = combined_adata.obs[sample_key].unique()
        de_results = sc.get.rank_genes_groups_df(combined_adata, group=groups[0])

    print(f"\n✓ DE analysis complete")
    print(f"\nTop {min(10, n_genes)} differentially expressed genes:")
    print(de_results.head(10)[['names', 'logfoldchanges', 'pvals_adj']])

    return de_results.head(n_genes)


# ============================================================================
# SECTION 7: GIFT-SEQ INTEGRATION FOR TARGETED VARIANT DETECTION
# ============================================================================

def load_giftseq_data(h5_path: str) -> ad.AnnData:
    """
    Load GIFT-seq data from GIFTwrap pipeline output.

    Best Practice:
    - GIFT-seq provides targeted variant detection
    - Use PCR duplicate filtering for accuracy
    - Integrate with WTA data for spatial context

    Parameters:
    -----------
    h5_path : str
        Path to counts.N.h5 file from GIFTwrap pipeline

    Returns:
    --------
    giftseq_adata : AnnData
        GIFT-seq count matrix
    """
    print(f"\n{'='*80}")
    print("LOADING GIFT-SEQ DATA")
    print(f"{'='*80}")

    print(f"Loading from: {h5_path}")
    giftseq_adata = gw.read_h5_file(h5_path)

    print(f"✓ GIFT-seq data loaded")
    print(f"  Cells: {giftseq_adata.n_obs:,}")
    print(f"  Features: {giftseq_adata.n_vars:,}")
    print(f"  Probes: {giftseq_adata.var.probe.nunique()}")

    # Show available layers
    if giftseq_adata.layers:
        print(f"  Available layers: {list(giftseq_adata.layers.keys())}")

    return giftseq_adata


def filter_giftseq_by_pcr_threshold(giftseq_adata: ad.AnnData,
                                     threshold: int = 5) -> ad.AnnData:
    """
    Filter GIFT-seq data by PCR duplicate threshold.

    Best Practice:
    - PCR duplicate filtering reduces false positives
    - Threshold of 3-5 recommended for VisiumHD
    - Higher threshold = more stringent filtering

    Parameters:
    -----------
    giftseq_adata : AnnData
        GIFT-seq data
    threshold : int
        Minimum number of unique reads (PCR duplicates)

    Returns:
    --------
    giftseq_adata : AnnData
        Filtered GIFT-seq data
    """
    print(f"\n{'='*80}")
    print(f"FILTERING BY PCR THRESHOLD ({threshold})")
    print(f"{'='*80}")

    layer_key = f'X_pcr_threshold_{threshold}'

    if layer_key in giftseq_adata.layers:
        print(f"  Applying PCR threshold filter...")
        original_counts = giftseq_adata.X.sum()
        giftseq_adata.X = giftseq_adata.layers[layer_key]
        filtered_counts = giftseq_adata.X.sum()

        pct_retained = 100 * filtered_counts / original_counts
        print(f"✓ Filter applied")
        print(f"  Original UMIs: {original_counts:,.0f}")
        print(f"  Filtered UMIs: {filtered_counts:,.0f}")
        print(f"  Retained: {pct_retained:.1f}%")
    else:
        print(f"  ⚠ Layer '{layer_key}' not found, using default X matrix")

    return giftseq_adata


def call_genotypes(giftseq_adata: ad.AnnData) -> ad.AnnData:
    """
    Call discrete genotypes from GIFT-seq UMI counts.

    Best Practice:
    - Genotype calling assigns WT/HET/ALT labels
    - Filter low-quality genotypes with gw.pp.filter_gapfills()
    - Validate against known genotypes when possible

    Parameters:
    -----------
    giftseq_adata : AnnData
        GIFT-seq data

    Returns:
    --------
    giftseq_adata : AnnData
        GIFT-seq data with genotypes in .obsm['genotype']
    """
    print(f"\n{'='*80}")
    print("CALLING GENOTYPES")
    print(f"{'='*80}")

    # Filter low-quality gapfills
    print("  Filtering low-quality gapfills...")
    gw.pp.filter_gapfills(giftseq_adata, min_cells=10)

    # Call genotypes
    print("  Calling discrete genotypes...")
    giftseq_adata = gw.tl.call_genotypes(giftseq_adata)

    print(f"✓ Genotypes called")
    print(f"  Genotype matrix: {giftseq_adata.obsm['genotype'].shape}")

    # Show example genotype distribution
    probe = giftseq_adata.var.probe.unique()[0]
    if probe in giftseq_adata.obsm['genotype'].columns:
        genotype_counts = giftseq_adata.obsm['genotype'][probe].value_counts()
        print(f"\n  Example: {probe}")
        print(genotype_counts)

    return giftseq_adata


def integrate_giftseq_with_spatial(sdata: sd.SpatialData,
                                   giftseq_adata: ad.AnnData,
                                   resolution: str = '016um') -> sd.SpatialData:
    """
    Integrate GIFT-seq data with spatial WTA data.

    Best Practice:
    - Join by matching cell barcodes
    - Creates 'gf_square_XXXum' tables in SpatialData
    - Enables spatial visualization of genotypes

    Parameters:
    -----------
    sdata : SpatialData
        Spatial WTA data
    giftseq_adata : AnnData
        GIFT-seq variant data
    resolution : str
        Resolution to integrate at

    Returns:
    --------
    sdata : SpatialData
        SpatialData with integrated GIFT-seq data
    """
    print(f"\n{'='*80}")
    print("INTEGRATING GIFT-SEQ WITH SPATIAL DATA")
    print(f"{'='*80}")

    print(f"  Joining at resolution: {resolution}")
    sdata = gw.sp.join_with_wta(sdata, giftseq_adata)

    gf_table_name = f'gf_square_{resolution}'

    if gf_table_name in sdata.tables:
        print(f"✓ Integration complete")
        print(f"  GIFT-seq table: {gf_table_name}")
        print(f"  Cells with variants: {sdata.tables[gf_table_name].n_obs:,}")
        print(f"  Variant features: {sdata.tables[gf_table_name].n_vars:,}")
    else:
        print(f"  ⚠ Integration failed - check cell barcode overlap")

    return sdata


def plot_genotypes_spatial(sdata: sd.SpatialData,
                          probe: str,
                          resolution: str = '016um',
                          save_path: str = None):
    """
    Visualize genotypes on spatial coordinates.

    Best Practice:
    - Use GIFTwrap's built-in spatial genotype plotting
    - Overlay on H&E image for context
    - Color by genotype (WT/HET/ALT)

    Parameters:
    -----------
    sdata : SpatialData
        SpatialData with integrated GIFT-seq
    probe : str
        Probe name to visualize
    resolution : str
        Resolution for plotting
    save_path : str
        Optional path to save figure
    """
    print(f"\n{'='*80}")
    print(f"PLOTTING GENOTYPES: {probe}")
    print(f"{'='*80}")

    fig = gw.sp.plot_genotypes(
        sdata,
        probe,
        image_name="hires_image",
        resolution=int(resolution.replace('um', ''))
    )

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved to {save_path}")

    plt.show()


# ============================================================================
# SECTION 6: ADVANCED SPATIAL ANALYSIS
# ============================================================================

def compute_neighborhood_enrichment(sdata: sd.SpatialData,
                                   resolution: str = '016um',
                                   cluster_key: str = 'spatio_expression_coclustering') -> pd.DataFrame:
    """
    Compute neighborhood enrichment between clusters.

    Best Practice:
    - Identifies which clusters are co-localized
    - Important for understanding tissue organization
    - Use permutation testing for significance

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData with clusters
    resolution : str
        Resolution for analysis
    cluster_key : str
        Column name with cluster assignments

    Returns:
    --------
    enrichment : pd.DataFrame
        Neighborhood enrichment scores
    """
    print(f"\n{'='*80}")
    print("COMPUTING NEIGHBORHOOD ENRICHMENT")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    print("  Running permutation test...")
    sq.gr.nhood_enrichment(table, cluster_key=cluster_key, n_perms=1000)

    # Plot enrichment heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sq.pl.nhood_enrichment(table, cluster_key=cluster_key, ax=ax)
    plt.tight_layout()
    plt.show()

    print(f"✓ Neighborhood enrichment computed")

    return table.uns[f'{cluster_key}_nhood_enrichment']['zscore']


def compute_ligand_receptor_interactions(sdata: sd.SpatialData,
                                        resolution: str = '016um',
                                        cluster_key: str = 'spatio_expression_coclustering',
                                        n_pairs: int = 50):
    """
    Compute ligand-receptor interaction scores.

    Best Practice:
    - Uses CellPhoneDB database
    - Identifies potential cell-cell communication
    - Focus on significant interactions (FDR < 0.05)

    Parameters:
    -----------
    sdata : SpatialData
        Input SpatialData with clusters
    resolution : str
        Resolution for analysis
    cluster_key : str
        Column name with cluster assignments
    n_pairs : int
        Number of top interactions to show
    """
    print(f"\n{'='*80}")
    print("COMPUTING LIGAND-RECEPTOR INTERACTIONS")
    print(f"{'='*80}")

    table_name = f'square_{resolution}'
    table = sdata.tables[table_name]

    print("  Running CellPhoneDB analysis...")
    sq.gr.ligrec(
        table,
        n_perms=1000,
        cluster_key=cluster_key,
        copy=False,
        use_raw=False,
        transmitter_params={'categories': 'ligand'},
        receiver_params={'categories': 'receptor'}
    )

    # Plot top interactions
    fig, ax = plt.subplots(figsize=(12, 8))
    sq.pl.ligrec(table, cluster_key=cluster_key, n_pairs=n_pairs, ax=ax)
    plt.tight_layout()
    plt.show()

    print(f"✓ Ligand-receptor analysis complete")


# ============================================================================
# SECTION 7: EXAMPLE WORKFLOW
# ============================================================================

def example_workflow():
    """
    Complete example workflow for multi-sample VisiumHD analysis.

    This demonstrates the recommended order of operations for joint analysis
    of two tissue sections from the same sample, including integration,
    batch correction, and comparative analysis with GIFT-seq.
    """
    print(f"\n{'='*80}")
    print("MULTI-SAMPLE VISIUMHD ANALYSIS WORKFLOW")
    print(f"{'='*80}")
    print("""
    This example demonstrates best practices for jointly analyzing two
    VisiumHD tissue sections with SpatialData, squidpy, and GIFT-seq.

    Use Case: Analyzing two portions of the same tissue to compare
    spatial patterns, cell type distributions, and genetic variants.

    NOTE: Update file paths for your own data!
    """)

    # ========================================================================
    # STEP 1: LOAD MULTIPLE SAMPLES
    # ========================================================================

    # Example paths (UPDATE THESE!)
    sample_paths = {
        'section_A': "/path/to/spaceranger/section_A/outs",
        'section_B': "/path/to/spaceranger/section_B/outs"
    }
    giftseq_paths = {
        'section_A': "/path/to/giftwrap/section_A/counts.1.h5",
        'section_B': "/path/to/giftwrap/section_B/counts.1.h5"
    }
    output_dir = "./visiumhd_multisample_output"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "="*80)
    print("STEP 1: LOADING MULTIPLE SAMPLES")
    print("="*80)
    print("Loading two tissue sections for joint analysis...")

    # Uncomment to run:
    # # Load both samples
    # sample_dict = load_multiple_samples(sample_paths)
    #
    # # Cache each sample to ZARR for efficient reloading
    # for sample_name, sdata in sample_dict.items():
    #     zarr_path = f"{output_dir}/{sample_name}_spatial_data.zarr"
    #     sample_dict[sample_name] = cache_to_zarr(sdata, zarr_path, reload=True)
    #
    # sdata_A = sample_dict['section_A']
    # sdata_B = sample_dict['section_B']

    # ========================================================================
    # STEP 2: INDIVIDUAL QC AND PREPROCESSING
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 2: INDIVIDUAL QC AND PREPROCESSING")
    print("="*80)
    print("Performing QC on each sample separately before integration...")

    # Uncomment to run:
    # # Process Section A
    # sdata_A = compute_qc_metrics(sdata_A, resolution='016um')
    # plot_qc_spatial(sdata_A, resolution='016um',
    #                save_prefix=f"{output_dir}/section_A_qc")
    #
    # # Optionally crop to tissue region
    # # sdata_A = crop_to_tissue_region(sdata_A,
    # #                                 x_min=5000, x_max=40000,
    # #                                 y_min=5000, y_max=40000)
    #
    # # Process Section B
    # sdata_B = compute_qc_metrics(sdata_B, resolution='016um')
    # plot_qc_spatial(sdata_B, resolution='016um',
    #                save_prefix=f"{output_dir}/section_B_qc")
    #
    # # Optionally crop to tissue region
    # # sdata_B = crop_to_tissue_region(sdata_B,
    # #                                 x_min=5000, x_max=40000,
    # #                                 y_min=5000, y_max=40000)

    # ========================================================================
    # STEP 3: CONCATENATE AND INTEGRATE SAMPLES
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 3: CONCATENATE AND INTEGRATE SAMPLES")
    print("="*80)
    print("Merging samples and performing batch correction...")

    # Uncomment to run:
    # # Concatenate expression matrices from both samples
    # combined_adata = concatenate_spatial_tables(
    #     sample_dict,
    #     resolution='016um',
    #     batch_key='sample'
    # )
    #
    # # Perform batch correction with Harmony
    # combined_adata = integrate_samples_batch_correction(
    #     combined_adata,
    #     batch_key='sample',
    #     use_harmony=True
    # )
    #
    # print(f"Integrated {combined_adata.n_obs} bins from {len(sample_dict)} samples")

    # ========================================================================
    # STEP 4: JOINT DIMENSIONALITY REDUCTION AND CLUSTERING
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 4: JOINT DIMENSIONALITY REDUCTION AND CLUSTERING")
    print("="*80)
    print("Computing joint UMAP and clustering across both samples...")

    # Uncomment to run:
    # # Visualize integration quality
    # plot_integrated_umap(combined_adata,
    #                     batch_key='sample',
    #                     save_path=f"{output_dir}/integrated_umap.png")
    #
    # # Cluster jointly across samples
    # sc.tl.leiden(combined_adata, resolution=0.5, key_added='leiden_joint')
    #
    # # Visualize clusters
    # fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    # sc.pl.umap(combined_adata, color='leiden_joint', ax=axes[0], show=False)
    # sc.pl.umap(combined_adata, color='sample', ax=axes[1], show=False)
    # plt.tight_layout()
    # plt.savefig(f"{output_dir}/joint_clustering.png", dpi=300, bbox_inches='tight')
    # plt.close()

    # ========================================================================
    # STEP 5: CELL TYPE ANNOTATION
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 5: CELL TYPE ANNOTATION")
    print("="*80)
    print("Annotating cell types in integrated data...")

    # Uncomment to run:
    # # Option 1: Annotate using marker genes
    # marker_genes = {
    #     'T_cells': ['CD3D', 'CD3E', 'CD8A'],
    #     'B_cells': ['CD79A', 'MS4A1'],
    #     'Myeloid': ['CD14', 'CD68', 'LYZ'],
    #     'Epithelial': ['EPCAM', 'KRT18']
    # }
    # combined_adata = annotate_celltypes_by_markers(combined_adata, marker_genes)
    #
    # # Option 2: Use reference-based annotation
    # # ref_adata = sc.read_h5ad("/path/to/reference.h5ad")
    # # combined_adata = annotate_celltypes_from_reference(combined_adata, ref_adata)
    #
    # # Visualize cell types
    # sc.pl.umap(combined_adata, color='celltype',
    #           save=f"{output_dir}/celltypes_umap.png")

    # ========================================================================
    # STEP 6: COMPARE COMPOSITION BETWEEN SAMPLES
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 6: COMPARE COMPOSITION BETWEEN SAMPLES")
    print("="*80)
    print("Quantifying differences in cell type composition...")

    # Uncomment to run:
    # # Compare cell type proportions
    # composition_comparison = compare_samples_composition(
    #     combined_adata,
    #     celltype_key='celltype',
    #     sample_key='sample',
    #     save_path=f"{output_dir}/composition_comparison.png"
    # )
    #
    # print("\nComposition differences:")
    # print(composition_comparison)
    #
    # # Statistical test for composition differences
    # from scipy.stats import chi2_contingency
    # contingency = pd.crosstab(combined_adata.obs['celltype'],
    #                          combined_adata.obs['sample'])
    # chi2, pval, dof, expected = chi2_contingency(contingency)
    # print(f"\nChi-square test: p-value = {pval:.4e}")

    # ========================================================================
    # STEP 7: DIFFERENTIAL EXPRESSION BETWEEN SAMPLES
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 7: DIFFERENTIAL EXPRESSION BETWEEN SAMPLES")
    print("="*80)
    print("Finding genes differentially expressed between sections...")

    # Uncomment to run:
    # # Find sample-specific markers
    # de_results = differential_expression_between_samples(
    #     combined_adata,
    #     sample_key='sample',
    #     save_path=f"{output_dir}/differential_expression.csv"
    # )
    #
    # # Visualize top markers
    # top_genes = de_results.head(20)['names'].tolist()
    # sc.pl.dotplot(combined_adata, top_genes, groupby='sample',
    #              save=f"{output_dir}/de_dotplot.png")

    # ========================================================================
    # STEP 8: ANNOTATION TRANSFER
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 8: ANNOTATION TRANSFER BETWEEN SAMPLES")
    print("="*80)
    print("Transferring annotations from one sample to another...")

    # Uncomment to run:
    # # Transfer cell type annotations from section A to section B
    # # Useful when one section has better annotation confidence
    # sdata_B = transfer_annotations_between_samples(
    #     sdata_A, sdata_B,
    #     annotation_key='celltype',
    #     resolution='016um'
    # )
    #
    # # Compare original vs transferred annotations
    # plot_celltypes_spatial(sdata_B, resolution='016um',
    #                       save_path=f"{output_dir}/section_B_transferred_celltypes.png")

    # ========================================================================
    # STEP 9: SPATIAL PATTERN COMPARISON
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 9: SPATIAL PATTERN COMPARISON")
    print("="*80)
    print("Comparing spatial patterns between samples...")

    # Uncomment to run:
    # # Compute spatial autocorrelation for each sample
    # sdata_A = compute_spatial_features(sdata_A, resolution='016um')
    # spatial_genes_A = compute_spatial_autocorrelation(sdata_A, resolution='016um')
    #
    # sdata_B = compute_spatial_features(sdata_B, resolution='016um')
    # spatial_genes_B = compute_spatial_autocorrelation(sdata_B, resolution='016um')
    #
    # # Find genes with spatial patterns in both samples
    # common_spatial_genes = set(spatial_genes_A.index) & set(spatial_genes_B.index)
    # print(f"\nFound {len(common_spatial_genes)} genes with spatial patterns in both samples")
    #
    # # Side-by-side spatial visualization
    # compare_spatial_patterns(
    #     sample_dict,
    #     genes=['CD3D', 'CD68', 'EPCAM'],  # Update with your genes of interest
    #     resolution='016um',
    #     save_prefix=f"{output_dir}/spatial_comparison"
    # )
    #
    # # Compute neighborhood enrichment for each sample
    # enrichment_A = compute_neighborhood_enrichment(sdata_A, resolution='016um')
    # enrichment_B = compute_neighborhood_enrichment(sdata_B, resolution='016um')

    # ========================================================================
    # STEP 10: MULTI-SAMPLE GIFT-SEQ INTEGRATION
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 10: MULTI-SAMPLE GIFT-SEQ INTEGRATION")
    print("="*80)
    print("Integrating GIFT-seq variant data from both samples...")

    # Uncomment to run:
    # # Load GIFT-seq data for both samples
    # giftseq_A = load_giftseq_data(giftseq_paths['section_A'])
    # giftseq_B = load_giftseq_data(giftseq_paths['section_B'])
    #
    # # Filter by PCR duplicates
    # giftseq_A = filter_giftseq_by_pcr_threshold(giftseq_A, threshold=5)
    # giftseq_B = filter_giftseq_by_pcr_threshold(giftseq_B, threshold=5)
    #
    # # Call genotypes
    # giftseq_A = call_genotypes(giftseq_A)
    # giftseq_B = call_genotypes(giftseq_B)
    #
    # # Integrate with spatial data
    # sdata_A = integrate_giftseq_with_spatial(sdata_A, giftseq_A, resolution='016um')
    # sdata_B = integrate_giftseq_with_spatial(sdata_B, giftseq_B, resolution='016um')
    #
    # # Compare genotype distributions between samples
    # for probe in giftseq_A.var.probe.unique()[:3]:  # First 3 probes
    #     fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    #
    #     # Plot Section A
    #     plot_genotypes_spatial(sdata_A, probe, resolution='016um',
    #                          ax=axes[0], title=f'Section A - {probe}')
    #
    #     # Plot Section B
    #     plot_genotypes_spatial(sdata_B, probe, resolution='016um',
    #                          ax=axes[1], title=f'Section B - {probe}')
    #
    #     plt.tight_layout()
    #     plt.savefig(f"{output_dir}/genotype_comparison_{probe}.png",
    #                dpi=300, bbox_inches='tight')
    #     plt.close()
    #
    # # Concatenate GIFT-seq data for joint analysis
    # giftseq_A.obs['sample'] = 'section_A'
    # giftseq_B.obs['sample'] = 'section_B'
    # giftseq_combined = ad.concat([giftseq_A, giftseq_B], merge='same')
    #
    # # Compare genotype frequencies between samples
    # for probe in giftseq_combined.var.probe.unique()[:5]:
    #     probe_mask = giftseq_combined.var.probe == probe
    #     contingency = pd.crosstab(
    #         giftseq_combined.obs['sample'],
    #         giftseq_combined[:, probe_mask].obs['genotype']
    #     )
    #     print(f"\n{probe} genotype distribution:")
    #     print(contingency)
    #     print(contingency / contingency.sum(axis=1).values[:, None])  # Percentages

    # ========================================================================
    # STEP 11: EXPORT RESULTS
    # ========================================================================

    print("\n" + "="*80)
    print("STEP 11: EXPORT RESULTS")
    print("="*80)

    # Uncomment to run:
    # # Save processed SpatialData objects
    # sdata_A.write(f"{output_dir}/section_A_processed.zarr", overwrite=True)
    # sdata_B.write(f"{output_dir}/section_B_processed.zarr", overwrite=True)
    #
    # # Save integrated AnnData
    # combined_adata.write_h5ad(f"{output_dir}/integrated_wta.h5ad")
    #
    # # Save GIFT-seq data
    # if 'gf_square_016um' in sdata_A.tables:
    #     sdata_A.tables['gf_square_016um'].write_h5ad(
    #         f"{output_dir}/section_A_giftseq.h5ad"
    #     )
    # if 'gf_square_016um' in sdata_B.tables:
    #     sdata_B.tables['gf_square_016um'].write_h5ad(
    #         f"{output_dir}/section_B_giftseq.h5ad"
    #     )
    #
    # # Export combined GIFT-seq
    # giftseq_combined.write_h5ad(f"{output_dir}/combined_giftseq.h5ad")

    print(f"\n{'='*80}")
    print("MULTI-SAMPLE WORKFLOW COMPLETE!")
    print(f"{'='*80}")
    print(f"""
    Your multi-sample analysis is complete! Results saved to: {output_dir}/

    Key outputs:
    - section_A_processed.zarr / section_B_processed.zarr: Processed SpatialData
    - integrated_wta.h5ad: Batch-corrected integrated expression matrix
    - combined_giftseq.h5ad: Combined GIFT-seq variant data
    - *_comparison.png: Comparative visualizations
    - differential_expression.csv: Sample-specific markers

    Recommended next steps:
    1. Examine composition_comparison.png for cell type differences
    2. Review differential_expression.csv for sample-specific genes
    3. Compare spatial patterns in spatial_comparison_*.png
    4. Analyze genotype_comparison_*.png for variant distributions
    5. Use combined datasets for further downstream analysis
    """)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║        VisiumHD Analysis Demo: Best Practices Guide                ║
    ║                                                                    ║
    ║    SpatialData + squidpy + GIFT-seq Integration                   ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝

    This script provides a comprehensive template for analyzing VisiumHD
    spatial transcriptomics data with targeted variant detection.

    To use this script:
    1. Update file paths in example_workflow()
    2. Uncomment code blocks you want to run
    3. Adjust parameters for your dataset

    For interactive analysis, import functions individually:
        from visiumhd_analysis_demo import load_visiumhd_data, compute_qc_metrics

    """)

    # Run example workflow (with commented code)
    example_workflow()

    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║                     Happy Analyzing! 🔬                            ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)