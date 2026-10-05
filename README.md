# <PAPER TITLE>

Analysis code and composite atomic models accompanying:

> <AUTHORS> (<YEAR>). *<PAPER TITLE>*. <JOURNAL / bioRxiv>. doi:<PAPER DOI>

Archived release: [![DOI](https://zenodo.org/badge/DOI/<ZENODO DOI>.svg)](https://doi.org/<ZENODO DOI>)

In-cell cryo-ET, subtomogram averaging and hyperspectral CLEM of
*Chroococcidiopsis thermalis* grown under white light (WL) and far-red light (FRL).

## Contents

| File | Purpose | Main input | Figure |
|---|---|---|---|
| `notebooks/pbs_row_assignment_graph_clustering.ipynb` | Clean a RELION 5 template-matching particle list by assigning phycobilisome (PBS) row identities (spatial + angular graph clustering), gap filling, duplicate removal, row-wise halfsets | particle STAR, boundary masks | <Fig. X> |
| `scripts/assign_spline_membrane_angles.py` | Assign per-spline median Euler angle priors from MPicker picks to a STOPGAP spline motivelist | STOPGAP STAR, MPicker angle file | <Fig. X> |
| `notebooks/compare_two_particle_row_lists.ipynb` | Row-aware comparison of WL and FRL PBS particle lists: row lengths, within-row pair distances / g(r), within-row angles, row spacing | two particle STARs | <Fig. X> |
| `notebooks/WLFRL_particle_distribution.ipynb` | Test for self-affinity of wl-PBS vs frl-PBS in FRL tomograms (between-row neighbour graph, row-label permutation null) | row-assigned STARs | <Fig. X> |
| `notebooks/WL_FRL_intermem_distances.ipynb` | Inter-thylakoid (stromal gap) distances from surface morphometrics output, WL vs FRL | morphometrics CSV / VTP | <Fig. X> |
| `notebooks/supercomplex_map_geometry_comparison.ipynb` | Relative PBS–PSII geometry measured from segmented MRC maps, compared across structures | segmented MRC volumes | <Fig. X> |
| `notebooks/pigment_donor_acceptor_distances.ipynb` | Pairwise donor→acceptor pigment distances from a PDB/mmCIF model | atomic model (see `models/`) | <Fig. X> |
| `notebooks/hsCLEM_analysis.ipynb` | Low-temperature hyperspectral fluorescence emission spectra, WL vs FRL | per-cell spectra CSV | <Fig. X> |
| `models/` | Composite atomic models (see `models/README.md`) | | <Fig. X> |

## Installation

```bash
git clone https://github.com/<ORG>/<REPO>.git
cd <REPO>
conda env create -f environment.yml
conda activate <ENV NAME>
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

<Sofie van Dorst>, <sofie.vandorst@unibas.ch>
