#!/usr/bin/env python
"""
assign_spline_membrane_angles.py
===========================
Assigns membrane normal and row orientation angle priors to interpolated
spline particles in a STOPGAP motivelist, using manually picked Euler angles
from MPicker as the source.

Usage
-----
    python assign_spline_mem_angles.py <spline_motl.star> <mpicker_angles.txt>

Arguments
---------
spline_motl.star
    STOPGAP STAR file produced by sg_motl_batch_spline. Particles are
    grouped by their '_object' field, which identifies the spline they
    were interpolated from.

mpicker_angles.txt
    Tab-separated coordinate and angle file exported from MPicker.
    Expected columns (header row skipped):
        X  Y  Z  rot  tilt  psi  class
    The 'class' column must match the '_object' values in the motivelist
    to associate each spline with its manually picked orientation.

Angle convention conversion
---------------------------
MPicker angles are converted to STOPGAP ZXZ Euler angle convention as:
    phi = -90 - rot
    psi =  90 - psi_MP
    the = -tilt

The median of the converted angles over all manual picks belonging to
each spline is then assigned to every interpolated particle on that spline.
Using the median rather than the mean provides robustness to outlier picks.

Output
------
A new STAR file named <spline_motl>_angs.star with updated phi, psi, the
columns. All other fields are unchanged.
"""

import sys
import argparse
from pathlib import Path

import pandas as pd


# ── Argument parsing ──────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Assign per-spline median Euler angles from MPicker to a STOPGAP motivelist.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("motl",      help="STOPGAP spline motivelist STAR file")
    parser.add_argument("mpicker",   help="MPicker Euler angles text file")
    parser.add_argument("--output",  default=None,
                        help="Output file path (default: <motl>_angs.star)")
    parser.add_argument("--skiprows-motl", type=int, default=20,
                        help="Header rows to skip in the motivelist (default: 20)")
    parser.add_argument("--skiprows-mpicker", type=int, default=1,
                        help="Header rows to skip in the MPicker file (default: 1)")
    return parser.parse_args()


# ── I/O ───────────────────────────────────────────────────────────────────────

MOTL_COLUMNS = [
    '_motl_idx', '_tomo_num', '_object', '_subtomo_num', '_halfset',
    '_orig_x', '_orig_y', '_orig_z', '_score',
    '_x_shift', '_y_shift', '_z_shift',
    '_phi', '_psi', '_the', '_class',
]

MPICKER_COLUMNS = ['X', 'Y', 'Z', 'rot', 'tilt', 'psi', 'class']

STOPGAP_HEADER = """\
data_stopgap_motivelist

loop_
_motl_idx
_tomo_num
_object
_subtomo_num
_halfset
_orig_x
_orig_y
_orig_z
_score
_x_shift
_y_shift
_z_shift
_phi
_psi
_the
_class

"""


def read_motl(path, skiprows):
    return pd.read_table(path, skiprows=skiprows, header=None,
                         sep=r'\s+', names=MOTL_COLUMNS)


def read_mpicker(path, skiprows):
    return pd.read_table(path, skiprows=skiprows, header=None,
                         names=MPICKER_COLUMNS)


def write_motl(df, path):
    with open(path, 'w') as f:
        f.write(STOPGAP_HEADER)
        df.to_csv(f, sep='\t', index=False, header=False, float_format='%.4f')


# ── Angle conversion and assignment ──────────────────────────────────────────

def convert_mpicker_angles(coords_mp):
    """Convert MPicker angles to STOPGAP ZXZ Euler convention (in-place)."""
    coords_mp['_phi'] = -90.0 - coords_mp['rot']
    coords_mp['_psi'] =  90.0 - coords_mp['psi']
    coords_mp['_the'] = -coords_mp['tilt']
    return coords_mp


def compute_median_angles(coords_mp):
    """Return per-spline median phi/psi/the from MPicker picks."""
    coords_mp['spline_ID'] = coords_mp['class'].astype(str)
    return (coords_mp
            .groupby('spline_ID')[['_phi', '_psi', '_the']]
            .median()
            .reset_index()
            .round(4))


def assign_angles(motl, median_angles):
    """Merge median angles into motivelist by spline ID."""
    motl['spline_ID'] = motl['_object'].astype(str)
    motl = motl.merge(median_angles, on='spline_ID', how='left')
    # _phi/_psi/_the come out as _phi_x (original) and _phi_y (from median);
    # replace originals with median values
    for ang in ('phi', 'psi', 'the'):
        motl[f'_{ang}'] = motl[f'_{ang}_y']
    motl = motl.drop(columns=[f'_{a}_x' for a in ('phi','psi','the')] +
                              [f'_{a}_y' for a in ('phi','psi','the')] +
                              ['spline_ID'])
    return motl


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    motl      = read_motl(args.motl, args.skiprows_motl)
    coords_mp = read_mpicker(args.mpicker, args.skiprows_mpicker)

    coords_mp    = convert_mpicker_angles(coords_mp)
    median_angles = compute_median_angles(coords_mp)

    print("Per-spline median angles:")
    print(median_angles.to_string(index=False))

    motl = assign_angles(motl, median_angles)

    output_path = args.output or Path(args.motl).stem + '_angs.star'
    write_motl(motl, output_path)
    print(f"\nWrote {len(motl)} particles to: {output_path}")


if __name__ == "__main__":
    main()
