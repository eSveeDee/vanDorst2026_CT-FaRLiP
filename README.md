# Far-Red Light Photoacclimation Rewires Antenna-Photosystem Organization in Cyanobacterial Cells

Analysis code and composite atomic models accompanying:

> S. van Dorst, V.M. Selinger, D.J. Nürnberg, W. Wietrzynski, B.D. Engel (2026). **Far-Red Light Photoacclimation Rewires Antenna-Photosystem Organization in Cyanobacterial Cells**. <bioRxiv>. doi:<PAPER DOI>

Archived release: [![DOI](https://zenodo.org/badge/DOI/<ZENODO DOI>.svg)](https://doi.org/<ZENODO DOI>)

Scripts used for hsCLEM, subtomogram averaging, spatial analysis of particles, and pigment distance calculations.

## Contents

| File | Purpose | Main input |
|---|---|---|
| `notebooks/pbs_row_assignment_graph_clustering.ipynb` | Clean a RELION 5 template-matching particle list by assigning phycobilisome (PBS) row identities (spatial + angular graph clustering), gap filling, duplicate removal, row-wise halfsets | particle STAR, boundary masks 
| `scripts/assign_spline_membrane_angles.py` | Assign per-spline median Euler angle priors from MPicker picks to a STOPGAP spline motivelist | STOPGAP STAR, MPicker angle file 
| `notebooks/compare_two_particle_row_lists.ipynb` | Row-aware comparison of WL and FRL PBS particle lists: row lengths, within-row pair distances / g(r), within-row angles, row spacing | two particle STARs 
| `notebooks/WLFRL_particle_distribution.ipynb` | Test for self-affinity of wl-PBS vs frl-PBS in FRL tomograms (between-row neighbour graph, row-label permutation null) | row-assigned STARs 
| `notebooks/WL_FRL_intermem_distances.ipynb` | Inter-thylakoid (stromal gap) distances from surface morphometrics output, WL vs FRL | morphometrics CSV / VTP 
| `notebooks/supercomplex_map_geometry_comparison.ipynb` | Relative PBS–PSII geometry measured from segmented MRC maps, compared across structures | segmented MRC volumes 
| `notebooks/pigment_donor_acceptor_distances.ipynb` | Pairwise donor→acceptor pigment distances from a PDB/mmCIF model | atomic model (see `models/`) 
| `notebooks/hsCLEM_analysis.ipynb` | Low-temperature hyperspectral fluorescence emission spectra, WL vs FRL | per-cell spectra CSV 
| `models/` | Composite atomic models (see `models/README.md`) | 

## Installation

```bash
git clone https://github.com/eSveeDee/vanDorst2026_CT-FaRLiP.git
cd vanDorst2026_CT-FaRLiP
conda env create -f environment.yml
conda activate ct-farlip
jupyter lab
```

## Usage

Each notebook has a user-parameter block at the top; set input paths there and
run all cells. The script is run from the command line:

```bash
python scripts/assign_spline_membrane_angles.py <spline_motl.star> <mpicker_angles.txt>
```

## Data availability

| Data | Accession |
|---|---|
| Subtomogram averages | EMD-<XXXXX> |
| Tomograms / tilt series | EMPIAR-<XXXXX> |
| Composite models | this repository, `models/` |

## Licence

Code: MIT (`LICENSE`). Models: CC BY 4.0 (`models/README.md`).

## Contact

Sofie van Dorst, <sofie.vandorst@unibas.ch>
